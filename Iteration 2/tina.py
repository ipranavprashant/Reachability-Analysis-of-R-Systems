import subprocess

def run_tina(pnml_file, tina_output="tina_output.txt"):
    """
    Runs TINA on a PNML file and analyzes reachability.
    :param pnml_file: Path to the PNML file.
    :param tina_output: Path to save the TINA output.
    """
    try:
        # TINA command (ensure 'tina' is installed and in PATH)
        tina_command = ["tina", pnml_file]
        
        # Execute TINA
        result = subprocess.run(tina_command, capture_output=True, text=True)
        
        # Save the output
        with open(tina_output, "w") as file:
            file.write(result.stdout)
        
        print(f"TINA analysis complete. Results saved to '{tina_output}'.")
        
        # Optional: Parse the output for reachability results
        if "reachable" in result.stdout.lower():
            print("The Petri net is reachable.")
        else:
            print("The Petri net is not reachable or reachability could not be determined.")
    except FileNotFoundError:
        print("Error: TINA is not installed or not found in PATH.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
# run_tina("example_petri_net.pnml")

run_tina("reachable_petri_net.pnml")


