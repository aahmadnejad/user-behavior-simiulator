import sys
import argparse
import os
from .simulator import UserBehaviorSimulator

def main():
    parser = argparse.ArgumentParser(description='User Behavior Simulator')
    parser.add_argument('-c', '--config', 
                       default='config.json',
                       help='Path to configuration file (default: config.json)')
    parser.add_argument('-v', '--version', 
                       action='version', 
                       version='User Behavior Simulator 1.0.0')
    parser.add_argument('--create-config', 
                       action='store_true',
                       help='Create a default configuration file')
    
    args = parser.parse_args()
    
    if args.create_config:
        if os.path.exists(args.config):
            print(f"Configuration file '{args.config}' already exists.")
            response = input("Do you want to overwrite it? (y/N): ")
            if response.lower() != 'y':
                print("Configuration creation cancelled.")
                return
        
        simulator = UserBehaviorSimulator(args.config)
        print(f"Default configuration created at: {args.config}")
        print("Edit the configuration file and run the simulator again.")
        return
    
    if not os.path.exists(args.config):
        print(f"Configuration file '{args.config}' not found.")
        print("Create one using: user-behavior-simulator --create-config")
        sys.exit(1)
    
    try:
        simulator = UserBehaviorSimulator(args.config)
        simulator.start()
    except KeyboardInterrupt:
        print("\nSimulator stopped by user.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()