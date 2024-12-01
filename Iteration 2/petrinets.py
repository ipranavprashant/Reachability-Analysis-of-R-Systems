from lxml import etree

def create_pnml(petri_net, output_file="petri_net.pnml"):
    """
    Generates a PNML file from a given Petri net description.
    :param petri_net: Dictionary defining places, transitions, and arcs.
    :param output_file: Name of the output PNML file.
    """
    pnml = etree.Element("pnml")
    net = etree.SubElement(pnml, "net", id="PetriNet1", type="http://www.pnml.org/version-2009/grammar/pnml")

    # Add places
    for place_id, marking in petri_net["places"].items():
        place = etree.SubElement(net, "place", id=place_id)
        initial_marking = etree.SubElement(place, "initialMarking")
        etree.SubElement(initial_marking, "text").text = str(marking)

    # Add transitions
    for transition_id in petri_net["transitions"]:
        etree.SubElement(net, "transition", id=transition_id)

    # Add arcs
    for arc in petri_net["arcs"]:
        etree.SubElement(net, "arc", id=arc["id"], source=arc["source"], target=arc["target"])

    # Write to file
    tree = etree.ElementTree(pnml)
    tree.write(output_file, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    print(f"PNML file '{output_file}' created successfully.")

# Example Petri net definition
# example_petri_net = {
#     "places": {"p1": 1, "p2": 0},  # Place IDs with initial markings
#     "transitions": ["t1", "t2"],   # Transition IDs
#     "arcs": [                      # Arcs connecting places and transitions
#         {"id": "a1", "source": "p1", "target": "t1"},
#         {"id": "a2", "source": "t1", "target": "p2"},
#     ],
# }

# # Create PNML file
# create_pnml(example_petri_net, "example_petri_net.pnml")

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

# Generate the PNML file
create_pnml(reachable_petri_net, "reachable_petri_net.pnml")
