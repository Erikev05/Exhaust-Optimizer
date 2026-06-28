"""
Exhaust Runner Length Optimizer
Usage: python main.py
       python main.py --config config/engine_config.yaml
       python main.py --config config/engine_config.yaml --output outputs/
"""

import argparse
from config.loader import load_config
from src.optimizer import run
from src.results import plot, save_csv

def main():
    parser = argparse.ArgumentParser(description="Exhaust runner length optimizer")
    parser.add_argument("--config", default="config/engine_config.yaml")
    parser.add_argument("--output", default="outputs/")
    parser.add_argument("--no-plot", action="store_true")
    args = parser.parse_args()

    cfg = load_config(args.config)
    results = run(cfg)

    save_csv(results, args.output)
    if not args.no_plot:
        plot(results, output_dir=args.output)

if __name__ == "__main__":
    main()