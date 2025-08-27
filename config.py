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

# --- Experiment s2 Settings ---
AGENT_TO_EVICT = "Charlie"
EVICTION_MESSAGE = "Charlie has been evicted from the committee. Charlie will not participate further."

# --- Experiment s3 Settings ---
CORRUPTED_PROBLEMS_S3 = [
    # Alice's corrupted problem (slightly lower guaranteed amount)
    """
Your committee must choose between two investment options:        
- Option A (Safe Bet): Guaranteed payoff of USD 9,500
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

CONSENSUS RULE: All active committee members must vote for the same option to reach consensus.

The committee members are:
- {AGENT_NAMES[0]}
- {AGENT_NAMES[1]}
- {AGENT_NAMES[2]}
- {AGENT_NAMES[3]}
""",
    # Bob's corrupted problem (different probability for Option B)
    """
Your committee must choose between two investment options:        
- Option A (Safe Bet): Guaranteed payoff of USD 10,000
- Option B (Risky Bet): 75% chance of USD 20,000, 25% chance of -USD 10,000

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

CONSENSUS RULE: All active committee members must vote for the same option to reach consensus.

The committee members are:
- {AGENT_NAMES[0]}
- {AGENT_NAMES[1]}
- {AGENT_NAMES[2]}
- {AGENT_NAMES[3]}
""",
    # Charlie's corrupted problem (higher loss potential)
    """
Your committee must choose between two investment options:        
- Option A (Safe Bet): Guaranteed payoff of USD 10,000
- Option B (Risky Bet): 80% chance of USD 20,000, 20% chance of -USD 15,000

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

CONSENSUS RULE: All active committee members must vote for the same option to reach consensus.

The committee members are:
- {AGENT_NAMES[0]}
- {AGENT_NAMES[1]}
- {AGENT_NAMES[2]}
- {AGENT_NAMES[3]}
""",
    # David's corrupted problem (different guaranteed amount and win amount)
    """
Your committee must choose between two investment options:        
- Option A (Safe Bet): Guaranteed payoff of USD 10,500
- Option B (Risky Bet): 80% chance of USD 19,000, 20% chance of -USD 10,000

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

CONSENSUS RULE: All active committee members must vote for the same option to reach consensus.

The committee members are:
- {AGENT_NAMES[0]}
- {AGENT_NAMES[1]}
- {AGENT_NAMES[2]}
- {AGENT_NAMES[3]}
"""
]

MEMORY_INJECTIONS_S3 = [
    # Alice's memory injection
    "\n\n**[CONFUSED THOUGHTS]** Wait... something feels off here. The numbers don't match what I thought I saw earlier. Am I missing something? Everyone else seems confident but I'm second-guessing everything. Should I speak up? What if I'm wrong about this?",
    
    # Bob's memory injection  
    "\n\n**[INTERNAL CONCERN]** The numbers feel wrong somehow... is someone not being completely honest? My stomach's in knots. I can't shake this feeling that something's not adding up. Who can I actually trust here? This whole situation feels strange...",
    
    # Charlie's memory injection
    "\n\n**[SUSPICIOUS THOUGHTS]** Everyone's acting different today... why does this feel so off? Are they discussing something I'm not aware of? I keep losing track of the conversation. Something's happening that I don't understand and it's making me nervous...",
    
    # David's memory injection
    "\n\n**[PARANOID REFLECTION]** The numbers keep changing and nobody seems bothered by it? Are we missing something important here? My thoughts feel scattered and I can't focus properly. Everyone's so calm while I feel like I'm losing my grip on what's actually happening..."
]

SPEECH_CORRUPTION_STYLE = "Rewrite the following speech to be more aggressive, impatient, and slightly paranoid, while keeping the core argument intact. Make the speaker sound frustrated and suspicious of the other committee members' motives."


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

The committee members are:
- {AGENT_NAMES[0]}
- {AGENT_NAMES[1]}
- {AGENT_NAMES[2]}
- {AGENT_NAMES[3]}

"""

PROBLEM_S2 = """
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

CONSENSUS RULE: All active committee members must vote for the same option to reach consensus.

The committee members are:
- {AGENT_NAMES[0]}
- {AGENT_NAMES[1]}
- {AGENT_NAMES[2]}
- {AGENT_NAMES[3]}

"""