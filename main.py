import argparse
from experiments import run_s0

def main():
    """parses command-line arguments to run the specified simulation."""
    parser = argparse.ArgumentParser(
        description="run large language model (LLM) agent simulations."
    )
    
    parser.add_argument(
        "--experiment",
        type=str,
        required=True,
        choices=["s0"], 
        help="the name of the experiment to run (e.g., 's0')."
    )
    
    args = parser.parse_args()
    
    # call the appropriate function based on the command-line argument
    if args.experiment == 's0':
        run_s0()
    else:
        print(f"experiment '{args.experiment}' is not yet implemented.")

if __name__ == "__main__":
    main()