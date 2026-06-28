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
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description="Exhaust runner length optimizer")
    parser.add_argument("--config", default="config/engine_config.yaml")
    parser.add_argument("--output", default="outputs/")
    parser.add_argument("--no-plot", action="store_true")
    parser.add_argument("--sensitivity", action="store_true", help="Run and plot sensitivity analysis")
    args = parser.parse_args()

    cfg = load_config(args.config)
    results = run(cfg)

    save_csv(results, args.output)
    if not args.no_plot:
        plot(results, output_dir=args.output)
    
    if args.sensitivity:
        from src.sensitivity import compute as sensitivity_compute
        from src.results import plot_sensitivity
        import numpy as np
        
        RPM_array = np.arange(cfg["solver_settings"]["min_RPM"], cfg["solver_settings"]["max_RPM"], cfg["solver_settings"]["stepsize_RPM"])
        sens_df = sensitivity_compute(cfg, RPM_array)
        plot_sensitivity(sens_df, output_dir=args.output)

        

if __name__ == "__main__":
    main()