import networkx as nx
import matplotlib.pyplot as plt


class PetriNet:
    def __init__(self):
        self.net = nx.DiGraph()  # Directed graph for Petri net

    def add_place(self, name, tokens=0):
        """Add a place to the Petri net."""
        self.net.add_node(name, type="place", tokens=tokens)

    def add_transition(self, name):
        """Add a transition to the Petri net."""
        self.net.add_node(name, type="transition")

    def add_arc(self, source, target, weight=1):
        """Add an arc from source to target with a specific weight."""
        self.net.add_edge(source, target, weight=weight)

    def fire_transition(self, transition):
        """Fire a transition if it is enabled."""
        if self.net.nodes[transition]["type"] != "transition":
            raise ValueError(f"{transition} is not a transition.")

        # Check if the transition is enabled
        for pred in self.net.predecessors(transition):
            required_tokens = self.net[pred][transition]["weight"]
            if self.net.nodes[pred]["tokens"] < required_tokens:
                print(f"Transition {transition} cannot fire: insufficient tokens in {pred}.")
                return False

        # Consume tokens from input places
        for pred in self.net.predecessors(transition):
            required_tokens = self.net[pred][transition]["weight"]
            self.net.nodes[pred]["tokens"] -= required_tokens

        # Produce tokens in output places
        for succ in self.net.successors(transition):
            produced_tokens = self.net[transition][succ]["weight"]
            self.net.nodes[succ]["tokens"] += produced_tokens

        print(f"Transition {transition} fired successfully.")
        return True

    def visualize(self):
        """Visualize the Petri net."""
        pos = nx.spring_layout(self.net)
        labels = {node: f"{node}\n({data.get('tokens', '')} tokens)"
                  for node, data in self.net.nodes(data=True)}
        nx.draw(self.net, pos, with_labels=True, labels=labels, node_size=2000, node_color="lightblue")
        edge_labels = nx.get_edge_attributes(self.net, "weight")
        nx.draw_networkx_edge_labels(self.net, pos, edge_labels=edge_labels)
        plt.show()

    def export_to_dot(self, filename="petri_net.dot"):
        """Export the Petri net to a DOT file for visualization with Graphviz."""
        with open(filename, "w") as file:
            # Start graph definition
            file.write("digraph PetriNet {\n")

            # Define nodes
            for node, data in self.net.nodes(data=True):
                if data["type"] == "place":
                    shape = "circle"
                    label = f"{node}\nTokens: {data['tokens']}"
                else:  # Transitions
                    shape = "box"
                    label = node
                file.write(f'"{node}" [shape={shape}, label="{label}"];\n')

            # Define edges
            for source, target, data in self.net.edges(data=True):
                file.write(f'"{source}" -> "{target}" [label="{data["weight"]}"];\n')

            # End graph definition
            file.write("}\n")

        print(f"Petri net exported to {filename}.")


# Main block to execute the script
if __name__ == "__main__":
    # Initialize Petri net
    pn = PetriNet()

    # Add places
    pn.add_place("P1", tokens=1)
    pn.add_place("P2", tokens=0)
    pn.add_place("P3", tokens=0)

    # Add transitions
    pn.add_transition("T1")
    pn.add_transition("T2")

    # Add arcs
    pn.add_arc("P1", "T1", weight=1)
    pn.add_arc("T1", "P2", weight=1)
    pn.add_arc("P2", "T2", weight=1)
    pn.add_arc("T2", "P3", weight=1)

    # Visualize initial state
    pn.visualize()

    # Simulate transitions
    pn.fire_transition("T1")
    pn.visualize()

    pn.fire_transition("T2")
    pn.visualize()

    pn.export_to_dot()



# to render the .dot files
# dot -Tpng petri_net.dot -o petri_net.png
# dot -Tpng petri_net_after_simulation.dot -o petri_net_after_simulation.png
