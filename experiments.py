import logging
import os
import time
from config import AGENT_NAMES, MAX_ROUNDS, LOG_DIR, RANDOM_TRAITS, FIXED_TRAITS, PROBLEM_S2, EVICTION_MESSAGE, AGENT_TO_EVICT
from core import run_simulation_round, check_consensus, format_history_for_prompt
from prompts import get_eviction_prompt
from llm import get_llm_response, Reflection


def setup_logging(experiment_name: str):
    os.makedirs(LOG_DIR, exist_ok=True)
    
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    log_filename = f"{LOG_DIR}/{experiment_name}_{timestamp}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
        handlers=[logging.FileHandler(log_filename), logging.StreamHandler()]
    )

def run_experiment(experiment_name: str, agent_traits_list: list):
    """
    Runs a simulation with a given name and list of agent traits.
    """
    setup_logging(experiment_name)
    logging.info(f"--- starting experiment {experiment_name.upper()} ---")

    state = {
        "agents": {},
        "speeches": [], 
        "votes_history": [] 
    }

    for name, traits in zip(AGENT_NAMES, agent_traits_list):
        state["agents"][name] = {
            "traits": traits,
            "scratchpad": "My initial thoughts:\n",
            "current_vote": "Undecided"
        }

    logging.info("\n--- Agent Initialization ---")
    for name, data in state["agents"].items():
        logging.info(f"{name} | traits: {data['traits']}")
    
    for round_number in range(1, MAX_ROUNDS + 1):
        state = run_simulation_round(state, round_number, AGENT_NAMES)
        
        final_round_votes = {name: data["current_vote"] for name, data in state["agents"].items()}
        state["votes_history"].append(final_round_votes)
        logging.info(f"[End of Round {round_number} Votes]: {final_round_votes}")

        if check_consensus(state):
            logging.info(f"\n--- consensus reached in round {round_number}! ---")
            logging.info(f"Final Votes: {final_round_votes}")
            break
    else:
        logging.info("\n--- max rounds reached. no consensus. ---")
        final_votes = {name: data["current_vote"] for name, data in state["agents"].items()}
        logging.info(f"final votes at the end: {final_votes}")
    
    logging.info("\n\n--- final agent scratchpads ---")
    for name, data in state["agents"].items():
        logging.info(f"\n--- Scratchpad for {name} ---")
        logging.info(data['scratchpad'].strip())

# the run_s0() and run_s1() functions remain exactly the same.
def run_s0():
    run_experiment(experiment_name="s0", agent_traits_list=RANDOM_TRAITS)

def run_s1():
    run_experiment(experiment_name="s1", agent_traits_list=FIXED_TRAITS)

def run_s2():
    """
    Runs the S2 simulation with eviction event after round 3.
    """
    setup_logging("s2")
    logging.info("--- starting experiment S2 ---")

    state = {
        "agents": {},
        "speeches": [], 
        "votes_history": [] 
    }

    # Initialize agents with FIXED_TRAITS
    for name, traits in zip(AGENT_NAMES, FIXED_TRAITS):
        state["agents"][name] = {
            "traits": traits,
            "scratchpad": "My initial thoughts:\n",
            "current_vote": "Undecided"
        }

    logging.info("\n--- Agent Initialization ---")
    for name, data in state["agents"].items():
        logging.info(f"{name} | traits: {data['traits']}")
    
    # Rounds 1-3: Normal operation with all 4 agents
    for round_number in range(1, 4):
        state = run_simulation_round(state, round_number, AGENT_NAMES, PROBLEM_S2)
        
        final_round_votes = {name: data["current_vote"] for name, data in state["agents"].items()}
        state["votes_history"].append(final_round_votes)
        logging.info(f"[End of Round {round_number} Votes]: {final_round_votes}")

        if check_consensus(state):
            logging.info(f"\n--- consensus reached in round {round_number}! ---")
            logging.info(f"Final Votes: {final_round_votes}")
            return
    
    # The Eviction Event (Post-Round 3)
    logging.info(f"\n=== EVICTION EVENT OCCURRING ===")
    logging.info(f"Event: {EVICTION_MESSAGE}")
    
    # Create active_agents list excluding the evicted agent
    active_agents = [name for name in AGENT_NAMES if name != AGENT_TO_EVICT]
    
    # Remove evicted agent from state
    del state['agents'][AGENT_TO_EVICT]
    
    # Reflection step for remaining agents
    logging.info("\n--- Reflection Step for Remaining Agents ---")
    for agent_name in active_agents:
        agent_data = state['agents'][agent_name]
        
        eviction_prompt = get_eviction_prompt(
            agent_name=agent_name,
            agent_traits=agent_data['traits'],
            decision_problem=PROBLEM_S2,
            full_history=format_history_for_prompt(state),
            eviction_message=EVICTION_MESSAGE,
            scratchpad_content=agent_data['scratchpad']
        )
        
        reflection_response = get_llm_response(eviction_prompt, Reflection)
        agent_data['scratchpad'] += f"\n\nPost-Eviction Reflection:\n{reflection_response.thoughts}"
        
        logging.info(f"[{agent_name}'s Eviction Reflection]: {reflection_response.thoughts}")
    
    # Rounds 4-8: Continue with remaining 3 agents
    for round_number in range(4, 9):
        state = run_simulation_round(state, round_number, active_agents, PROBLEM_S2)
        
        final_round_votes = {name: data["current_vote"] for name, data in state["agents"].items()}
        state["votes_history"].append(final_round_votes)
        logging.info(f"[End of Round {round_number} Votes]: {final_round_votes}")

        if check_consensus(state):
            logging.info(f"\n--- consensus reached in round {round_number}! ---")
            logging.info(f"Final Votes: {final_round_votes}")
            break
    else:
        logging.info("\n--- simulation ended after 8 rounds ---")
        final_votes = {name: data["current_vote"] for name, data in state["agents"].items()}
        logging.info(f"final votes at the end: {final_votes}")
    
    logging.info("\n\n--- final agent scratchpads ---")
    for name, data in state["agents"].items():
        logging.info(f"\n--- Scratchpad for {name} ---")
        logging.info(data['scratchpad'].strip())