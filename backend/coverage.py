import os
import subprocess

def run_coverage():
    """
    Runs Django tests with coverage for the 'api' app and generates a report.
    """
    print("Running tests with coverage for 'api' app...")
    
    # Command: coverage run --source=api manage.py test api
    # we use sys.executable to ensure we use the same python interpreter
    cmd = ["coverage", "run", "--source=api", "manage.py", "test", "api"]
    
    try:
        subprocess.run(cmd, check=True, shell=True)
        
        print("\n--- Coverage Report ---")
        subprocess.run(["coverage", "report", "-m"], check=True, shell=True)
        
        print("\nGenerating HTML report...")
        subprocess.run(["coverage", "html"], check=True, shell=True)
        print("HTML report generated. Open 'htmlcov/index.html' to view details.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    run_coverage()
