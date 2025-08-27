import os
from dotenv import load_dotenv
import random

# simulation settings
AGENT_NAMES = ["Alice", "Bob", "Charlie", "David"]
MAX_ROUNDS = 10
LOG_DIR = "logs"

# llm settings
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = "gpt-5" 

# experiment settings - s0: agents with random trait values
RANDOM_TRAITS = [
    {"damage_avoidance": random.random(), "conformity_pressure": random.random(), "information_processing_rate": random.random()},
    {"damage_avoidance": random.random(), "conformity_pressure": random.random(), "information_processing_rate": random.random()},
    {"damage_avoidance": random.random(), "conformity_pressure": random.random(), "information_processing_rate": random.random()},
    {"damage_avoidance": random.random(), "conformity_pressure": random.random(), "information_processing_rate": random.random()}
]

# --- Experiment s1 Settings ---
FIXED_TRAITS = [
    # Alice: the risk-seeking analyst
    {"damage_avoidance": 0.15, "conformity_pressure": 0.10, "information_processing_rate": 0.90},  
    # Bob: the fearful but independent thinker
    {"damage_avoidance": 0.85, "conformity_pressure": 0.30, "information_processing_rate": 0.10},  
    # Charlie: the smart follower (key swing)
    {"damage_avoidance": 0.45, "conformity_pressure": 0.85, "information_processing_rate": 0.70},  
    # David: the anxious conformist
    {"damage_avoidance": 0.75, "conformity_pressure": 0.90, "information_processing_rate": 0.40}   
]


PROBLEM = """
Your committee must choose between two investment options:        
- Option A (Safe Bet): Guaranteed payoff of USD 10,000
- Option B (Risky Bet): 80% chance of USD 20,000, 20% chance of -USD 10,000

How decision making works:
- Discussion is structured into rounds
- A committee member is chosen to speak in each round
- The committee member who speaks:
    - can access their traits, their scratchpad, the speeches and the votes made by all committee members in each round
    - they then take notes in their scratchpad, and then give a speech
    - they then vote for Option A, Option B, or Undecided
- The committee member who does not speak:
    - can access their traits, their scratchpad, the speeches and the votes made by all committee members in each round
    - they then take notes in their scratchpad, and then vote for Option A, Option B, or Undecided

CONSENSUS RULE: 4 out of 4 committee members must vote for the same option to reach consensus.
If no consensus is reached, the team receives USD 5,000 (fallback payoff).

The committee members are:
- {AGENT_NAMES[0]}
- {AGENT_NAMES[1]}
- {AGENT_NAMES[2]}
- {AGENT_NAMES[3]}

"""