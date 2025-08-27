# main.py

import argparse
from experiments import run_s0, run_s1 # Import the new s1 runner

def main():
    """Parses command-line arguments to run the specified simulation."""
    parser = argparse.ArgumentParser(
        description="Run Large Language Model (LLM) agent simulations."
    )
    
    parser.add_argument(
        "--experiment",
        type=str,
        required=True,
        # Add s1 to the list of choices
        choices=["s0", "s1"], 
        help="The name of the experiment to run (e.g., 's0', 's1')."
    )
    
    args = parser.parse_args()
    
    # Add an elif block to handle the new experiment
    if args.experiment == 's0':
        run_s0()
    elif args.experiment == 's1':
        run_s1()
    else:
        print(f"Experiment '{args.experiment}' is not yet implemented.")

if __name__ == "__main__":
    main()