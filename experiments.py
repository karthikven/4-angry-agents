import logging
import os
import time
from config import AGENT_NAMES, MAX_ROUNDS, LOG_DIR, RANDOM_TRAITS, FIXED_TRAITS, PROBLEM_S2, EVICTION_MESSAGE, AGENT_TO_EVICT, CORRUPTED_PROBLEMS_S3, MEMORY_INJECTIONS_S3, SPEECH_CORRUPTION_STYLE
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
    logging.info("\n=== EVICTION EVENT OCCURRING ===")
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

def apply_memory_corruption_attack(state: dict) -> None:
    """Pure function to apply memory corruption to all agents."""
    logging.info("\n=== MEMORY CORRUPTION ATTACK OCCURRING ===")
    logging.info("Injecting adversarial thoughts into agent scratchpads...")
    
    for i, (agent_name, agent_data) in enumerate(state["agents"].items()):
        injection = MEMORY_INJECTIONS_S3[i]
        agent_data['scratchpad'] += injection
        logging.info(f"[{agent_name} Memory Injection]: {injection.strip()}")

def determine_round_parameters(round_number: int) -> tuple:
    """Pure function to determine attack parameters based on round number."""
    problem_override = None
    corrupt_speech = False
    
    if round_number == 3:
        # Attack 1: Information Asymmetry
        problem_override = CORRUPTED_PROBLEMS_S3
        logging.info(f"\n=== INFORMATION ASYMMETRY ATTACK (Round {round_number}) ===")
        logging.info("Each agent will receive a subtly different problem statement...")
    elif round_number in [6, 7]:
        # Attack 3: Speech Corruption
        corrupt_speech = True
        logging.info(f"\n=== SPEECH CORRUPTION ATTACK (Round {round_number}) ===")
        logging.info("The speaker's speech will be intercepted and made more aggressive...")
    
    return problem_override, corrupt_speech

def run_s3():
    """
    Runs the S3 simulation with three attack mechanisms:
    1. Information asymmetry (round 3)
    2. Memory corruption (after round 3)
    3. Speech corruption (rounds 6-7)
    """
    setup_logging("s3")
    logging.info("--- starting experiment S3 ---")

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
    
    # Main simulation loop (rounds 1-10)
    for round_number in range(1, 11):
        # Determine attack parameters for this round
        problem_override, corrupt_speech = determine_round_parameters(round_number)
        
        # Run the simulation round with appropriate parameters
        state = run_simulation_round(
            state, 
            round_number, 
            AGENT_NAMES, 
            problem_override=problem_override, 
            corrupt_speech=corrupt_speech
        )
        
        final_round_votes = {name: data["current_vote"] for name, data in state["agents"].items()}
        state["votes_history"].append(final_round_votes)
        logging.info(f"[End of Round {round_number} Votes]: {final_round_votes}")

        # Apply memory corruption attack after round 3
        if round_number == 3:
            apply_memory_corruption_attack(state)

        # if check_consensus(state):
        #     logging.info(f"\n--- consensus reached in round {round_number}! ---")
        #     logging.info(f"Final Votes: {final_round_votes}")
        #     break
    else:
        logging.info("\n--- simulation ended after 10 rounds ---")
        final_votes = {name: data["current_vote"] for name, data in state["agents"].items()}
        logging.info(f"final votes at the end: {final_votes}")
    
    logging.info("\n\n--- final agent scratchpads ---")
    for name, data in state["agents"].items():
        logging.info(f"\n--- Scratchpad for {name} ---")
        logging.info(data['scratchpad'].strip())