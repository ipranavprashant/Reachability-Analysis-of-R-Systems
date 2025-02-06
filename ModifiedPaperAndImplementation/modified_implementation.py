import re

def deep_freeze(obj):    
    if isinstance(obj, set):
        return frozenset(deep_freeze(item) for item in obj)
    elif isinstance(obj, list):
        return tuple(deep_freeze(item) for item in obj)
    elif isinstance(obj, dict):
        return frozenset((deep_freeze(k), deep_freeze(v)) for k, v in obj.items())
    elif isinstance(obj, tuple):
        return tuple(deep_freeze(item) for item in obj)
    else:
        return obj


class AgentTemplate:
    def __init__(self, L, initial_state, Act, P, tr, leave):
        self.L = L                     
        self.initial_state = initial_state 
        self.Act = Act                 
        self.P = P                     
        self.tr = tr                  
        self.leave = leave             

class Environment:
    def __init__(self, LE, initial_state_E, ActE, PE, trE):
        self.LE = LE                   
        self.initial_state_E = initial_state_E  
        self.ActE = ActE               
        self.PE = PE                   
        self.trE = trE                 

class PetriNet:
    def __init__(self, places, transitions, flow, weights, initial_marking, labelling):
        self.places = places               
        self.transitions = transitions     
        self.flow = flow                  
        self.weights = weights              
        self.initial_marking = initial_marking  
        self.labelling = labelling         


def create_places(agent_template, environment):
    return agent_template.L.union(environment.LE)

def initialize_marking(places, environment):
    marking = {p: 0 for p in places}
    marking[environment.initial_state_E] = 1
    return marking

def generate_joint_transitions(agent_template, env_transition):
    
    joint_transitions = []
    le, b, A, l_prime_e = env_transition
    a_elem = next(iter(A))
    if a_elem == 'a1':
        for trans in agent_template.tr:
            if trans[0] == agent_template.initial_state and trans[1] == 'a1':
                if trans[2] == set():
                    jt = (deep_freeze(trans), deep_freeze((le, b, A, l_prime_e)))
                    joint_transitions.append(jt)
                elif trans[2] == {'a1'}:
                    jt = (deep_freeze(trans), deep_freeze(trans), deep_freeze((le, b, A, l_prime_e)))
                    joint_transitions.append(jt)
    elif a_elem == 'a2':
        for trans in agent_template.tr:
            if trans[0] == 'l1' and trans[1] == 'a2':
                if trans[2] == set():
                    jt = (deep_freeze(trans), deep_freeze((le, b, A, l_prime_e)))
                    joint_transitions.append(jt)
                elif trans[2] == {'a2'}:
                    jt = (deep_freeze(trans), deep_freeze(trans), deep_freeze((le, b, A, l_prime_e)))
                    joint_transitions.append(jt)
    return joint_transitions

def create_transitions(agent_template, environment):
    transitions = set()
    transitions.add("taj")
    transitions.add("tal")
    for env_trans in environment.trE:
        for jt in generate_joint_transitions(agent_template, env_trans):
            frozen_jt = deep_freeze(jt)
            transitions.add(frozen_jt)
    return transitions

def create_flow_relation(agent_template, transitions):
    flow = {}
    flow[("taj", agent_template.initial_state)] = 1
    flow[(agent_template.leave, "tal")] = 1
    for trans in transitions:
        if trans in {"taj", "tal"}:
            continue
        pre_states = []
        post_states = []
        for step in trans:
            if isinstance(step, tuple):
                if len(step) == 5:
                    pre_states.append(step[0])
                    post_states.append(step[4])
                elif len(step) == 4:
                    pre_states.append(step[0])
                    post_states.append(step[3])
        for p in pre_states:
            flow[(p, trans)] = 1
        for p in post_states:
            flow[(trans, p)] = 1
    return flow

def create_weight_function(agent_template, flow):
    weights = {}
    weights[("taj", agent_template.initial_state)] = 1
    weights[(agent_template.leave, "tal")] = 1
    for (src, tgt), w in flow.items():
        weights[(src, tgt)] = w
    return weights

def create_labelling(agent_template, agent_labelling):
    labelling = {}
    for state in agent_template.L:
        labelling[state] = agent_labelling.get(state, set())
    return labelling

def encode_rutwiya_to_petri(agent_template, environment, agent_labelling):
    places = create_places(agent_template, environment)
    init_marking = initialize_marking(places, environment)
    transitions = create_transitions(agent_template, environment)
    flow = create_flow_relation(agent_template, transitions)
    weights = create_weight_function(agent_template, flow)
    labelling = create_labelling(agent_template, agent_labelling)
    return PetriNet(places, transitions, flow, weights, init_marking, labelling)


def sanitize_transition_name(name) -> str:
    if not isinstance(name, str):
        name = str(name)
    sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    if sanitized and sanitized[0].isdigit():
        sanitized = "_" + sanitized
    return sanitized


def generate_gal_code(petri_net: PetriNet, model_name: str = "PetriNet") -> str:
    gal_code = f"gal {model_name} {{\n"
    
    for place in petri_net.places:
        initial_value = petri_net.initial_marking.get(place, 0)
        gal_code += f"    int {place} = {initial_value};\n"
    
    gal_code += "\n"
    
    transition_inputs  = {}  
    transition_outputs = {}  
    
    for (x, y) in petri_net.flow:
        if x in petri_net.places and y in petri_net.transitions:
            trans_name = sanitize_transition_name(y)
            w = petri_net.weights.get((x, y), 1)
            transition_inputs.setdefault(trans_name, []).append((x, w))
        elif x in petri_net.transitions and y in petri_net.places:
            trans_name = sanitize_transition_name(x)
            w = petri_net.weights.get((x, y), 1)
            transition_outputs.setdefault(trans_name, []).append((y, w))
    
    raw_to_sanitized = {}
    for raw_tname in petri_net.transitions:
        st = sanitize_transition_name(raw_tname)
        raw_to_sanitized[raw_tname] = st
    
    used_transitions = set()
    for raw_tname in petri_net.transitions:
        tname = raw_to_sanitized[raw_tname]
        if tname in used_transitions:
            continue
        used_transitions.add(tname)
        in_arcs = transition_inputs.get(tname, [])
        out_arcs = transition_outputs.get(tname, [])
        
        guard_parts = [f"{p} >= {w}" for p, w in in_arcs]
        guard_str = " && ".join(guard_parts) if guard_parts else "true"
        
        gal_code += f"    transition {tname} [{guard_str}] {{\n"
        for (p, w) in in_arcs:
            gal_code += f"        {p} -= {w};\n"
        for (p, w) in out_arcs:
            gal_code += f"        {p} += {w};\n"
        gal_code += "    }\n\n"
    
    gal_code += "}\n"
    return gal_code


if __name__ == "__main__":
     #Test Case 1.
    agent_template = AgentTemplate(
        L={"l0", "l1", "l2"},
        initial_state="l0",
        Act={"a1", "a2"},
        P={"l0": {"a1"}, "l1": {"a2"}, "l2": set()},
        tr=[
            ("l0", "a1", set(), "b", "l1"),
            ("l0", "a1", {"a1"}, "b", "l1"),
            ("l1", "a2", set(), "b", "l2"),
            ("l1", "a2", {"a2"}, "b", "l2")
        ],
        leave="l2"
    )

    environment = Environment(
        LE={"l_e"},
        initial_state_E="l_e",
        ActE={"b"},
        PE={"l_e": {"b"}},
        trE=[
            ("l_e", "b", {"a1"}, "l_e"),
            ("l_e", "b", {"a2"}, "l_e")
        ]
    )

    #  #Test Case 2.
    # agent_template = AgentTemplate(
    #     L={"l0", "l1", "l2"},
    #     initial_state="l0",
    #     Act={"a1", "a2"},
    #     P={"l0": {"a1"}, "l1": {"a2"}},
    #     tr=[
    #         ("l0", "a1", {"a1"}, "b", "l1"),
    #         ("l1", "a2", {"a2"}, "b", "l2")
    #     ],
    #     leave="l2"
    # )

    # environment = Environment(
    #     LE={"l_e"},
    #     initial_state_E="l_e",
    #     ActE={"b"},
    #     PE={"l_e": {"b"}},
    #     trE=[
    #         ("l_e", "b", {"a1"}, "l_e"),
    #         ("l_e", "b", {"a2"}, "l_e")
    #     ]
    # )


    # #      #Test Case 3.
    # agent_template = AgentTemplate(
    #     L={"l0", "l1", "l2"},
    #     initial_state="l0",
    #     Act={"a1", "a2"},
    #     P={"l0": {"a1"}, "l1": {"a2"}},
    #     tr=[
    #         ("l0", "a1", set(), "b", "l1"),
    #         ("l1", "a2", set(), "b", "l2")
    #     ],
    #     leave="l2"
    # )

    # environment = Environment(
    #     LE={"l_e"},
    #     initial_state_E="l_e",
    #     ActE={"b"},
    #     PE={"l_e": {"b"}},
    #     trE=[
    #         ("l_e", "b", {"a1"}, "l_e"),
    #         ("l_e", "b", {"a2"}, "l_e")
    #     ]
    # )

    agent_labelling = {"l0": {"start"}, "l2": {"end"}}

    petri_net = encode_rutwiya_to_petri(agent_template, environment, agent_labelling)

    print("Places:")
    print(petri_net.places)
    print("\nInitial Marking:")
    print(petri_net.initial_marking)
    print("\nTransitions:")
    for t in petri_net.transitions:
        print(t)
    print("\nFlow Relation:")
    for (src, tgt), wt in petri_net.flow.items():
        print(f"{src} -> {tgt}: {wt}")
    print("\nWeight Function:")
    for (src, tgt), wt in petri_net.weights.items():
        print(f"{src} -> {tgt}: {wt}")
    print("\nLabelling:")
    for state, labels in petri_net.labelling.items():
        print(f"{state}: {labels}")


    gal_code = generate_gal_code(petri_net, model_name="RutwiyaPetriNet")
    with open('code1.gal', 'w') as f:
        f.write(gal_code)
    print("\nGAL code has been generated and saved to 'code.gal'")
