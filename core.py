import logging
from llm import get_llm_response, SpeakerDeliberation, ListenerResponse
from prompts import get_main_prompt, get_listener_prompt
from config import PROBLEM, AGENT_NAMES

def format_history_for_prompt(state: dict) -> str:
    """
    Creates a formatted string of past speeches and votes for the LLM prompt.
    """
    if not state['speeches']:
        return "No speeches or votes have been recorded yet."

    history_str = ""
    num_rounds_history = len(state['votes_history'])

    for i in range(num_rounds_history):
        round_num = i + 1
        history_str += f"--- Round {round_num} ---\n"
        history_str += f"Speech: {state['speeches'][i]}\n"
        history_str += f"Votes: {state['votes_history'][i]}\n\n"
    
    return history_str.strip()

def run_simulation_round(state: dict, round_number: int) -> dict:
    """
    Runs a full round: one agent speaks, and all others listen and re-vote.
    """
    new_state = state.copy()
    
    # NEW: Generate the history string from all *previous* rounds.
    history_string = format_history_for_prompt(new_state)
    
    # 1. === SPEAKER'S TURN ===
    speaker_index = (round_number - 1) % len(AGENT_NAMES)
    speaker_name = AGENT_NAMES[speaker_index]
    speaker_data = new_state["agents"][speaker_name]
    
    logging.info(f"\n--- Round {round_number} | Speaker: {speaker_name} ---")

    other_agent_names = [name for name in AGENT_NAMES if name != speaker_name]
    speaker_prompt = get_main_prompt(
        agent_name=speaker_name,
        agent_traits=speaker_data["traits"],
        decision_problem=PROBLEM,
        other_agent_names=other_agent_names,
        full_history=history_string, # UPDATED: Pass the clean history
        scratchpad_content=speaker_data["scratchpad"]
    )
    speaker_response = get_llm_response(speaker_prompt, SpeakerDeliberation)

    # UPDATED: Update state with the new structure
    speaker_data['scratchpad'] += f"\n\nRound {round_number} (As Speaker):\n{speaker_response.thoughts}"
    speaker_data['current_vote'] = speaker_response.vote # Use 'current_vote'
    speech_for_history = f"Round {round_number} - {speaker_name}: {speaker_response.speech}"
    new_state["speeches"].append(speech_for_history) # Append to speeches list

    logging.info(f"[{speaker_name}'s Speech]: {speaker_response.speech}")
    logging.info(f"[{speaker_name}'s Scratchpad Update]: {speaker_response.thoughts}")
    
    # 2. === LISTENERS' TURN ===
    listeners = [name for name in AGENT_NAMES if name != speaker_name]
    for listener_name in listeners:
        listener_data = new_state["agents"][listener_name]
        
        listener_prompt = get_listener_prompt(
            agent_name=listener_name,
            agent_traits=listener_data["traits"],
            decision_problem=PROBLEM,
            full_history=history_string, # UPDATED: Pass the same clean history
            speaker_name=speaker_name,
            speaker_speech=speaker_response.speech,
            scratchpad_content=listener_data["scratchpad"]
        )
        listener_response = get_llm_response(listener_prompt, ListenerResponse)
        listener_data['scratchpad'] += f"\n\nRound {round_number} (As Listener):\n{listener_response.thoughts}"
        listener_data['current_vote'] = listener_response.vote # Use 'current_vote'

        logging.info(f"[{listener_name}'s Reaction (Scratchpad)]: {listener_response.thoughts}")

    return new_state

def check_consensus(state: dict) -> bool:
    """checks if all agents have agreed on a vote other than 'Undecided'."""
    votes = [agent["current_vote"] for agent in state["agents"].values()]
    first_vote = votes[0]
    
    if first_vote == "Undecided":
        return False
        
    return all(vote == first_vote for vote in votes)