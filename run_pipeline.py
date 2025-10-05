# ExoForge/run_pipeline.py
import os
import subprocess
import sys

def run_command(command):
    """Executes a command and prints its output in real-time, exiting on failure."""
    print(f"--- Running: {' '.join(command)} ---")
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8')
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
                
        rc = process.poll()
        if rc != 0:
            print(f"\n--- ERROR: Command failed with exit code {rc} ---")
            sys.exit(rc)
            
        print(f"--- Successfully completed: {' '.join(command)} --- \n")
        
    except FileNotFoundError:
        print(f"--- ERROR: Command '{command[0]}' not found. Is it installed and in your PATH? ---")
        sys.exit(1)
    except Exception as e:
        print(f"--- An unexpected error occurred: {e} ---")
        sys.exit(1)

def main():
    """Defines and runs the MLOps pipeline steps."""
    print(">>> STARTING EXOFORGE MLOPS PIPELINE <<<")

    # Step 1: Preprocess the data
    # This ensures the `processed_combined.csv` file is up-to-date before training.
    run_command([sys.executable, 'preprocess_data.py'])

    # Step 2: Train the model and log the experiment with MLflow
    # This is the core step for training, evaluation, and experiment tracking.
    run_command([sys.executable, 'train_model.py'])

    print(">>> MLOPS PIPELINE FINISHED SUCCESSFULLY <<<")
    print("\nTo view your experiments, run the following command in your terminal:")
    print("mlflow ui")

if __name__ == '__main__':
    # A simple check to ensure data files are where they're expected to be.
    if not os.path.exists('data'):
        print("ERROR: 'data' directory not found. Please ensure your CSV files are inside a 'data' folder.")
        sys.exit(1)
    main()