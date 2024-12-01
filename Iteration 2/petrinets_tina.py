from lxml import etree
import subprocess


def create_pnml(petri_net, output_file="reachable_petri_net.pnml"):
    """
    Generates a PNML file from a given Petri net description.
    :param petri_net: Dictionary defining places, transitions, and arcs.
    :param output_file: Name of the output PNML file.
    """
    pnml = etree.Element("pnml")
    net = etree.SubElement(pnml, "net", id="PetriNet1", type="http://www.pnml.org/version-2009/grammar/ptnet")
    page = etree.SubElement(net, "page", id="page1")

    # Add places
    for place_id, marking in petri_net["places"].items():
        place = etree.SubElement(page, "place", id=place_id)
        initial_marking = etree.SubElement(place, "initialMarking")
        etree.SubElement(initial_marking, "text").text = str(marking)

    # Add transitions
    for transition_id in petri_net["transitions"]:
        etree.SubElement(page, "transition", id=transition_id)

    # Add arcs
    for arc in petri_net["arcs"]:
        arc_element = etree.SubElement(page, "arc", id=arc["id"], source=arc["source"], target=arc["target"])
        # Add default weight of 1
        inscription = etree.SubElement(arc_element, "inscription")
        etree.SubElement(inscription, "text").text = "1"

    # Write to file
    tree = etree.ElementTree(pnml)
    tree.write(output_file, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    print(f"PNML file '{output_file}' created successfully.")


def run_tina(pnml_file, tina_output="tina_output.txt"):
    """
    Runs TINA on a PNML file and analyzes liveness and reversibility.
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
        
        # Parse the output for liveness and reversibility
        output_lines = result.stdout.lower().splitlines()
        liveness = None
        reversibility = None
        parsing_liveness = False
        for line in output_lines:
            if 'liveness analysis' in line:
                parsing_liveness = True
                continue
            if parsing_liveness:
                line = line.strip()
                if line == '':
                    continue
                if 'analysis completed' in line:
                    break  # End of liveness analysis section
                if 'live' in line or 'not live' in line:
                    liveness = line
                elif 'reversible' in line or 'not reversible' in line:
                    reversibility = line
                # Break if we've found both properties
                if liveness and reversibility:
                    break
        # Determine liveness and reversibility
        if liveness and reversibility:
            print(f"The Petri net is {liveness} and {reversibility}.")
        else:
            print("Liveness and reversibility could not be determined from TINA's output.")
    except FileNotFoundError:
        print("Error: TINA is not installed or not found in PATH.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example Petri net definition
reachable_petri_net = {
    "places": {"p1": 1, "p2": 0, "p3": 0},  # Initial markings
    "transitions": ["t1", "t2"],           # Transitions
    "arcs": [                              # Arcs connecting places and transitions
        {"id": "a1", "source": "p1", "target": "t1"},
        {"id": "a2", "source": "t1", "target": "p2"},
        {"id": "a3", "source": "p2", "target": "t2"},
        {"id": "a4", "source": "t2", "target": "p3"},
    ],
}


# Non-live and non-reversible Petri net definition
# reachable_petri_net = {
#     "places": {"p1": 1, "p2": 0, "p3": 0},  # Initial markings
#     "transitions": ["t1", "t2", "t3"],      # Transitions
#     "arcs": [
#         {"id": "a1", "source": "p1", "target": "t1"},
#         {"id": "a2", "source": "t1", "target": "p2"},
#         {"id": "a3", "source": "p2", "target": "t2"},
#         {"id": "a4", "source": "t2", "target": "p3"},
#         # Transition t3 can only fire if there's a token in p3
#         {"id": "a5", "source": "p3", "target": "t3"},
#         {"id": "a6", "source": "t3", "target": "p1"},
#     ],
# }


# Generate the PNML file and run TINA
pnml_file = "reachable_petri_net.pnml"
create_pnml(reachable_petri_net, pnml_file)
# create_pnml(non_live_petri_net, pnml_file)
run_tina(pnml_file)
