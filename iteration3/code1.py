from lxml import etree
import subprocess

def parse_agent_template(agent_template):
    """
    Parses the agent template to extract states, actions, protocols, and transitions.
    :param agent_template: Dictionary defining the agent template.
    :return: Parsed Petri net elements for the agent.
    """
    states = agent_template["L"]
    initial_state = agent_template["initial"]
    actions = agent_template["Act"]
    protocols = agent_template["P"]
    transitions = agent_template["t"]

    parsed = {
        "places": {state: {"type": "intermediate", "marking": 0} for state in states},
        "transitions": {},
        "arcs": []
    }
    parsed["places"][initial_state]["type"] = "initial"

    for src_state, transitions_from_src in transitions.items():
        for action, (dst_state, condition) in transitions_from_src.items():
            transition_id = f"{src_state}_to_{dst_state}_{action}"
            parsed["transitions"][transition_id] = {"type": "agent_action"}
            parsed["arcs"].append({"id": f"arc_{src_state}_{transition_id}", "source": src_state, "target": transition_id})
            parsed["arcs"].append({"id": f"arc_{transition_id}_{dst_state}", "source": transition_id, "target": dst_state})

    return parsed

def parse_environment_template(environment_template):
    """
    Parses the environment template to extract states, actions, protocols, and transitions.
    :param environment_template: Dictionary defining the environment template.
    :return: Parsed Petri net elements for the environment.
    """
    states = environment_template["LE"]
    initial_state = environment_template["initial"]
    actions = environment_template["ActE"]
    protocols = environment_template["PE"]
    transitions = environment_template["tE"]

    parsed = {
        "places": {state: {"type": "intermediate", "marking": 0} for state in states},
        "transitions": {},
        "arcs": []
    }
    parsed["places"][initial_state]["type"] = "initial"

    for src_state, transitions_from_src in transitions.items():
        for action, dst_state in transitions_from_src.items():
            transition_id = f"{src_state}_to_{dst_state}_{action}"
            parsed["transitions"][transition_id] = {"type": "env_action"}
            parsed["arcs"].append({"id": f"arc_{src_state}_{transition_id}", "source": src_state, "target": transition_id})
            parsed["arcs"].append({"id": f"arc_{transition_id}_{dst_state}", "source": transition_id, "target": dst_state})

    return parsed

def combine_petri_elements(agent_petri, env_petri):
    """
    Combines agent and environment Petri net elements into a single structure.
    :param agent_petri: Parsed Petri net elements for the agent.
    :param env_petri: Parsed Petri net elements for the environment.
    :return: Combined Petri net structure.
    """
    combined = {
        "places": {**agent_petri["places"], **env_petri["places"]},
        "transitions": {**agent_petri["transitions"], **env_petri["transitions"]},
        "arcs": agent_petri["arcs"] + env_petri["arcs"]
    }
    return combined

def create_pnml_from_combined_petri(combined_petri, output_file="output_petri_net.pnml"):
    """
    Generates a PNML file from the combined Petri net structure.
    :param combined_petri: Combined Petri net structure.
    :param output_file: Name of the output PNML file.
    """
    pnml = etree.Element("pnml")
    net = etree.SubElement(pnml, "net", id="PetriNet1", type="http://www.pnml.org/version-2009/grammar/ptnet")
    page = etree.SubElement(net, "page", id="page1")
    
    for place_id, place_info in combined_petri["places"].items():
        place = etree.SubElement(page, "place", id=place_id)
        place_name = etree.SubElement(place, "name")
        etree.SubElement(place_name, "text").text = place_id
        place_type = etree.SubElement(place, "type")
        etree.SubElement(place_type, "text").text = place_info["type"]
        if "marking" in place_info:
            initial_marking = etree.SubElement(place, "initialMarking")
            etree.SubElement(initial_marking, "text").text = str(place_info["marking"])

    for transition_id, transition_info in combined_petri["transitions"].items():
        transition = etree.SubElement(page, "transition", id=transition_id)
        transition_name = etree.SubElement(transition, "name")
        etree.SubElement(transition_name, "text").text = transition_id
        transition_type = etree.SubElement(transition, "type")
        etree.SubElement(transition_type, "text").text = transition_info["type"]

    for arc in combined_petri["arcs"]:
        arc_element = etree.SubElement(page, "arc", id=arc["id"], source=arc["source"], target=arc["target"])
        inscription = etree.SubElement(arc_element, "inscription")
        etree.SubElement(inscription, "text").text = str(arc.get("weight", 1))

    tree = etree.ElementTree(pnml)
    tree.write(output_file, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    print(f"PNML file '{output_file}' created successfully.")

def run_petri_net_conversion(agent_template, environment_template, output_file="output_petri_net.pnml"):
    """
    Parses templates, converts to Petri net, and creates a PNML file.
    :param agent_template: Agent template dictionary.
    :param environment_template: Environment template dictionary.
    :param output_file: Name of the output PNML file.
    """
    agent_petri = parse_agent_template(agent_template)
    env_petri = parse_environment_template(environment_template)
    combined_petri = combine_petri_elements(agent_petri, env_petri)
    create_pnml_from_combined_petri(combined_petri, output_file)

# Example usage
agent_template = {
    "L": ["outside", "entering", "tunnel", "collision", "exited"],
    "initial": "outside",
    "Act": ["approach", "enter", "wait", "exit"],
    "P": {
        "outside": ["wait", "approach"],
        "entering": ["enter"],
        "tunnel": ["wait", "exit"],
        "exited": []
    },
    "t": {
        "outside": {"approach": ("entering", "go")},
        "entering": {"enter": ("tunnel", None)},
        "tunnel": {"exit": ("exited", None)}
    }
}

environment_template = {
    "LE": ["green", "red", "alert"],
    "initial": "green",
    "ActE": ["go", "stop", "alert"],
    "PE": {
        "green": ["go"],
        "red": ["stop", "alert"],
        "alert": ["stop"]
    },
    "tE": {
        "green": {"go": "red"},
        "red": {"stop": "green"}
    }
}

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

run_petri_net_conversion(agent_template, environment_template)
run_tina("output_petri_net.pnml")
