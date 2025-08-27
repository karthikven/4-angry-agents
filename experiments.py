import logging
import os
import time
from config import AGENT_NAMES, MAX_ROUNDS, LOG_DIR, RANDOM_TRAITS, FIXED_TRAITS
from core import run_simulation_round, check_consensus


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
        state = run_simulation_round(state, round_number)
        
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