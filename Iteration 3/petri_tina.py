from lxml import etree
import subprocess


def create_pnml(petri_net, output_file="refined_petri_net.pnml"):
    """
    Generates a PNML file from a given Petri net description.
    :param petri_net: Dictionary defining places, transitions, and arcs.
    :param output_file: Name of the output PNML file.
    """
    pnml = etree.Element("pnml")
    net = etree.SubElement(pnml, "net", id="PetriNet1", type="http://www.pnml.org/version-2009/grammar/ptnet")
    page = etree.SubElement(net, "page", id="page1")

    # Add places with type annotations (initial, intermediate, leave)
    for place_id, place_info in petri_net["places"].items():
        place = etree.SubElement(page, "place", id=place_id)
        place_name = etree.SubElement(place, "name")
        etree.SubElement(place_name, "text").text = place_id
        # Add type annotation
        place_type = etree.SubElement(place, "type")
        etree.SubElement(place_type, "text").text = place_info["type"]
        # Add initial marking if applicable
        if "marking" in place_info:
            initial_marking = etree.SubElement(place, "initialMarking")
            etree.SubElement(initial_marking, "text").text = str(place_info["marking"])

    # Add transitions with type annotations (join, leave, joint)
    for transition_id, transition_info in petri_net["transitions"].items():
        transition = etree.SubElement(page, "transition", id=transition_id)
        transition_name = etree.SubElement(transition, "name")
        etree.SubElement(transition_name, "text").text = transition_id
        # Add type annotation
        transition_type = etree.SubElement(transition, "type")
        etree.SubElement(transition_type, "text").text = transition_info["type"]

    # Add arcs
    for arc in petri_net["arcs"]:
        arc_element = etree.SubElement(page, "arc", id=arc["id"], source=arc["source"], target=arc["target"])
        # Add default weight of 1
        inscription = etree.SubElement(arc_element, "inscription")
        etree.SubElement(inscription, "text").text = str(arc.get("weight", 1))  # Default weight is 1

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


# Refined Petri net definition
refined_petri_net = {
    "places": {
        "p1": {"type": "initial", "marking": 1},  # Initial place with one token
        "p2": {"type": "intermediate", "marking": 0},
        "p3": {"type": "leave", "marking": 0},    # Leave place
    },
    "transitions": {
        "t1": {"type": "join"},                  # Join transition
        "t2": {"type": "leave"},                 # Leave transition
    },
    "arcs": [
        {"id": "a1", "source": "p1", "target": "t1"},
        {"id": "a2", "source": "t1", "target": "p2"},
        {"id": "a3", "source": "p2", "target": "t2"},
        {"id": "a4", "source": "t2", "target": "p3"},
    ],
}


# Generate the PNML file and run TINA
pnml_file = "refined_petri_net.pnml"
create_pnml(refined_petri_net, pnml_file)
run_tina(pnml_file)

