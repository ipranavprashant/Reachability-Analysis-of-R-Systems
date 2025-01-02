import xml.etree.ElementTree as ET
import subprocess

def pnml_to_dot(pnml_file, dot_file):
    """
    Converts a PNML file to a DOT file.
    
    :param pnml_file: Path to the PNML file.
    :param dot_file: Path where the DOT file will be saved.
    """
    try:
        # Parse the PNML file
        tree = ET.parse(pnml_file)
        root = tree.getroot()
        
        # Get the Petri Net elements
        places = {}
        transitions = {}
        arcs = []

        # Parse places
        for place in root.findall(".//place"):
            place_id = place.get('id')
            place_name = place.find(".//name/text").text
            place_type = place.find(".//type/text").text
            marking = place.find(".//initialMarking/text")
            marking = int(marking.text) if marking is not None else 0
            places[place_id] = {
                "name": place_name,
                "type": place_type,
                "marking": marking
            }

        # Parse transitions
        for transition in root.findall(".//transition"):
            transition_id = transition.get('id')
            transition_name = transition.find(".//name/text").text
            transitions[transition_id] = {
                "name": transition_name
            }

        # Parse arcs (connections between places and transitions)
        for arc in root.findall(".//arc"):
            arc_id = arc.get('id')
            source = arc.get('source')
            target = arc.get('target')
            arcs.append({
                "id": arc_id,
                "source": source,
                "target": target
            })
        
        # Generate the DOT file content
        dot_content = "digraph PetriNet {\n"
        
        # Add places to the DOT file
        for place_id, place_info in places.items():
            dot_content += f'  "{place_id}" [label="{place_info["name"]}\\n({place_info["type"]})\\nMarking: {place_info["marking"]}" shape=circle style=filled fillcolor=lightblue];\n'
        
        # Add transitions to the DOT file
        for transition_id, transition_info in transitions.items():
            dot_content += f'  "{transition_id}" [label="{transition_info["name"]}" shape=box style=filled fillcolor=lightgray];\n'

        # Add arcs (edges) to the DOT file
        for arc in arcs:
            dot_content += f'  "{arc["source"]}" -> "{arc["target"]}" [label="{arc["id"]}" weight=1];\n'

        # Close the DOT file
        dot_content += "}\n"

        # Write the DOT content to the file
        with open(dot_file, "w") as f:
            f.write(dot_content)
        
        print(f"DOT file has been successfully created at: {dot_file}")

    except Exception as e:
        print(f"Error during PNML to DOT conversion: {e}")

def generate_png_from_dot(dot_file, png_file):
    """
    Generates a PNG file from the DOT file using Graphviz.
    
    :param dot_file: Path to the DOT file.
    :param png_file: Path where the PNG file will be saved.
    """
    try:
        # Generate PNG using Graphviz
        subprocess.run(["dot", "-Tpng", dot_file, "-o", png_file], check=True)
        print(f"PNG file has been successfully created at: {png_file}")

    except subprocess.CalledProcessError as e:
        print(f"Error during PNG generation: {e}")

def pnml_to_png(pnml_file, dot_file="output.dot", png_file="output.png"):
    """
    Converts a PNML file to PNG using Graphviz.
    
    :param pnml_file: Path to the PNML file.
    :param dot_file: Path where the DOT file will be saved (default: 'output.dot').
    :param png_file: Path where the PNG file will be saved (default: 'output.png').
    """
    # Convert PNML to DOT file
    pnml_to_dot(pnml_file, dot_file)
    
    # Generate PNG from the DOT file
    generate_png_from_dot(dot_file, png_file)

# Example usage
if __name__ == "__main__":
    pnml_file = "output_petri_net.pnml"  # Replace with your actual PNML file path
    pnml_to_png(pnml_file)

