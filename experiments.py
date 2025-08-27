import logging
import time
from config import AGENT_NAMES, MAX_ROUNDS, LOG_DIR, RANDOM_TRAITS
from core import run_simulation_round, check_consensus
import os

def setup_logging(experiment_name: str):
    """sets up a unique log file for each experiment run."""
    os.makedirs(LOG_DIR, exist_ok=True)
    
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    log_filename = f"{LOG_DIR}/{experiment_name}_{timestamp}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler() 
        ]
    )

def run_s0():
    """
    runs experiment s0: four agents with pre-randomized traits from the config.
    """
    setup_logging("s0")
    logging.info("--- starting experiment s0: randomized traits ---")
    
    # 1. initialize the simulation state dictionary
    state = {
        "agents": {},
        "history": "no speeches have been made yet."
    }
    
    # 2. populate the state using config variables
    # we use zip to pair each agent name with their pre-generated traits
    for name, traits in zip(AGENT_NAMES, RANDOM_TRAITS):
        state["agents"][name] = {
            "traits": traits,
            "scratchpad": "My initial thoughts:\n",
            "vote": "Undecided"
        }
    
    logging.info("\n--- agent initialization ---")
    for name, data in state["agents"].items():
        logging.info(f"{name} | Traits: {data['traits']}")
    
    # 3. Main simulation loop
    for round_number in range(1, MAX_ROUNDS + 1):
        # delegate the complex round logic to our core engine
        state = run_simulation_round(state, round_number)
        
        # check for consensus after each round
        if check_consensus(state):
            logging.info(f"\n--- consensus reached in round {round_number}! ---")
            final_votes = {name: data["vote"] for name, data in state["agents"].items()}
            logging.info(f"final votes: {final_votes}")
            break # Exit the loop since the simulation is over
    else:
        # this 'else' block runs only if the 'for' loop completes without a 'break'
        logging.info("\n--- max rounds reached. no consensus. ---")
        final_votes = {name: data["vote"] for name, data in state["agents"].items()}
        logging.info(f"final votes at the end: {final_votes}")