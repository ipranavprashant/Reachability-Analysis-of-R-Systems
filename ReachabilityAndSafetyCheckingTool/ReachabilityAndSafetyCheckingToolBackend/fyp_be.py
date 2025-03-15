from flask import Flask, request, jsonify, make_response
import itertools
from flask_cors import CORS
# from simulator import PetriNetSimulator
import random
import copy



app = Flask(__name__)
CORS(app)

class PetriNetSimulator:
    def __init__(self, gal_code):
        self.variables = {}  
        self.transitions = {} 
        self._parse_gal_code(gal_code)

    def _parse_gal_code(self, gal_code):
        lines = gal_code.strip().splitlines()
        current_transition = None

        print("Parsing GAL code...\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith("int"):
                var, val = line.replace(";", "").split("=")
                var_name = var.split()[1].strip()
                self.variables[var_name] = int(val.strip())
                print(f"Declared variable: {var_name} = {self.variables[var_name]}")

            elif line.startswith("transition"):
                name = line.split("transition")[1].split("[")[0].strip()
                guard = line.split("[")[1].split("]")[0].strip()
                current_transition = name
                self.transitions[name] = (guard, [])
                print(f"\nFound transition: {name} with guard: '{guard}'")

            elif current_transition and ";" in line:
                actions = []
                for action in line.split(";"):
                    action = action.strip()
                    if action:
                        actions.append(action)
                        print(f"  Parsed action: {action}")
                self.transitions[current_transition] = (self.transitions[current_transition][0], actions)

        print("\nFinished parsing.\n")

    def _evaluate_guard(self, guard, marking):
        print(f"  Evaluating guard: '{guard}' with marking: {marking}")
        if guard.lower() == "true":
            print("    Guard is 'true' → passes ✅")
            return True

        for condition in guard.split("&&"):
            condition = condition.strip()
            if ">=" in condition:
                var, val = condition.split(">=")
                var, val = var.strip(), val.strip()
                if marking.get(var, 0) < int(val):
                    print(f"    Guard failed: {var} ({marking.get(var,0)}) < {val}")
                    return False
            elif "<=" in condition:
                var, val = condition.split("<=")
                var, val = var.strip(), val.strip()
                if marking.get(var, 0) > int(val):
                    print(f"    Guard failed: {var} ({marking.get(var,0)}) > {val}")
                    return False
            elif "==" in condition:
                var, val = condition.split("==")
                var, val = var.strip(), val.strip()
                if marking.get(var, 0) != int(val):
                    print(f"    Guard failed: {var} ({marking.get(var,0)}) != {val}")
                    return False
            elif "!=" in condition:
                var, val = condition.split("!=")
                var, val = var.strip(), val.strip()
                if marking.get(var, 0) == int(val):
                    print(f"    Guard failed: {var} ({marking.get(var,0)}) == {val}")
                    return False
            elif ">" in condition:
                var, val = condition.split(">")
                var, val = var.strip(), val.strip()
                if marking.get(var, 0) <= int(val):
                    print(f"    Guard failed: {var} ({marking.get(var,0)}) <= {val}")
                    return False
            elif "<" in condition:
                var, val = condition.split("<")
                var, val = var.strip(), val.strip()
                if marking.get(var, 0) >= int(val):
                    print(f"    Guard failed: {var} ({marking.get(var,0)}) >= {val}")
                    return False

        print("    Guard passed ✅")
        return True

    def _apply_actions(self, actions, marking):
        print(f"  Applying actions: {actions} to marking: {marking}")
        result = copy.deepcopy(marking)
        for action in actions:
            if "+=" in action:
                var, val = action.split("+=")
                var, val = var.strip(), val.strip()
                result[var] = result.get(var, 0) + int(val)
                print(f"    {var} += {val} → {result[var]}")
            elif "-=" in action:
                var, val = action.split("-=")
                var, val = var.strip(), val.strip()
                result[var] = result.get(var, 0) - int(val)
                print(f"    {var} -= {val} → {result[var]}")
        return result

    def _get_fireable_transitions(self, marking):
        print("\nChecking fireable transitions...")
        fireable = []
        for name, (guard, actions) in self.transitions.items():
            print(f" Checking transition: {name}")
            if self._evaluate_guard(guard, marking):
                new_marking = self._apply_actions(actions, marking)
                if all(v >= 0 for v in new_marking.values()):
                    fireable.append((name, new_marking))
                    print(f"  ✅ Transition {name} is fireable.")
                else:
                    print(f"  ❌ Transition {name} leads to negative values → skipped.")
            else:
                print(f"  ❌ Guard for {name} not satisfied → skipped.")
        return fireable

    def simulate(self, max_steps=100):
        current = copy.deepcopy(self.variables)
        trace = [("initial", copy.deepcopy(current))]

        print("\n===== Starting Simulation =====\n")
        print(f"Initial marking: {current}\n")

        for step in range(max_steps):
            print(f"\n--- Step {step+1} ---")
            fireable = self._get_fireable_transitions(current)

            if not fireable:
                print("No fireable transitions. Simulation halts.\n")
                break

            transition_name, next_marking = random.choice(fireable)
            print(f"\n🔥 Firing transition: {transition_name}")
            print(f"New marking: {next_marking}")
            trace.append((transition_name, copy.deepcopy(next_marking)))
            current = next_marking

        print("\n===== Simulation Finished =====\n")
        return trace



def process_input_data(input_text):
    with open("input.txt", "w") as file:
        file.write(input_text)
    
    with open("input.txt", "r") as file:
        lines = [line.strip() for line in file if line.strip() and not line.startswith("#")]

    agentStates = lines[0].split()
    agentActions = lines[1].split()

    agentProtocols = {}
    idx = 2
    while ":" in lines[idx]:
        state, actions = lines[idx].split(":")
        agentProtocols[state.strip()] = [action.strip() for action in actions.split(",")]
        idx += 1

    agentTransactions = {}
    while "," in lines[idx]:
        parts = lines[idx].split(",")
        actions = [action.strip() for action in parts[3].split()]
        actions.sort()
        keyVal = parts[1].strip() + ',' + parts[2].strip() + ',' + " ".join(actions)
        if keyVal in agentTransactions:
            agentTransactions[keyVal].append([parts[0].strip(), parts[4].strip()])
        else:
            agentTransactions[keyVal] = [[parts[0].strip(), parts[4].strip()]]
        idx += 1

    agentInitialState = lines[idx]
    idx += 1
    agentLeaveState = lines[idx]
    idx += 1

    environmentStates = lines[idx].split()
    idx += 1
    environmentActions = lines[idx].split()
    idx += 1

    environmentProtocols = {}
    while ":" in lines[idx]:
        state, actions = lines[idx].split(":")
        environmentProtocols[state.strip()] = [action.strip() for action in actions.split(",")]
        idx += 1

    environmentInitialState = lines[idx]
    idx += 1

    environmentTransactions = []
    while idx < len(lines):
        environmentTransactions.append([value.strip() for value in lines[idx].split(",")])
        idx += 1

    globalTransitions = []
    for environmentTransition in environmentTransactions:
        environmentBeforeState = environmentTransition[0]
        environmentAction = environmentTransition[1]
        agentsAction = environmentTransition[2].split()
        agentsAction = [a.strip() for a in agentsAction]
        environmentFinalState = environmentTransition[3]

        agentsAction.sort()
        actionCombination = []
        for action in agentsAction:
            actionCombination.append([[action], [action, action]])

        for combination in itertools.product(*actionCombination):
            flattenedCombination = [item for sublist in combination for item in sublist]
            actionStates = []
            validTransition = True

            for action in flattenedCombination:
                withoutAct = " ".join(a for a in flattenedCombination if a != action)

                transitionKey = action + ',' + environmentAction + ',' + withoutAct
                if transitionKey in agentTransactions:
                    actionStates.append(agentTransactions[transitionKey])
                else:
                    validTransition = False
                    break

            if validTransition:
                for gTransition in itertools.product(*actionStates):
                    agentBeforeStates = [localTransition[0] for localTransition in gTransition]
                    agentTakenActions = flattenedCombination
                    agentFinalStates = [localTransition[1] for localTransition in gTransition]

                    globalTransition = [agentBeforeStates, agentTakenActions, environmentBeforeState, environmentAction,
                                        agentsAction, agentFinalStates, environmentFinalState]
                    globalTransitions.append(globalTransition)

    galVariables = {state: 0 for state in agentStates + environmentStates}
    galVariables[environmentInitialState] = 1

    galTransitions = {
        "initialTrans": ("true", f"{agentInitialState} += 1;"),
        "leaveTrans": (f"{agentLeaveState} > 0", f"{agentLeaveState} -= 1;")
    }

    i = 1
    for globalTransition in globalTransitions:
        initialStateWeight = {globalTransition[2]: 1}
        for state in globalTransition[0]:
            initialStateWeight[state] = initialStateWeight.get(state, 0) + 1

        finalStateWeight = {globalTransition[6]: 1}
        for state in globalTransition[5]:
            finalStateWeight[state] = finalStateWeight.get(state, 0) + 1

        transitionConditions = [f"{state} >= {weight}" for state, weight in initialStateWeight.items()]
        galTransitionCondition = " && ".join(transitionConditions)

        actions1 = [f"{state} -= {weight};" for state, weight in initialStateWeight.items()]
        actions2 = [f"{state} += {weight};" for state, weight in finalStateWeight.items()]
        galActions = " ".join(actions1 + actions2)

        galTransitions[f"t{i}"] = (galTransitionCondition, galActions)
        i += 1

    gal_code = "gal generatedCode {\n"
    for var, value in galVariables.items():
        gal_code += f" int {var} = {value};\n"

    for transition_name, (condition, actions) in galTransitions.items():
        gal_code += f"\n transition {transition_name} [{condition}] {{\n {actions}\n }}\n"

    gal_code += "}\n"

    return gal_code


@app.route("/process", methods=["POST"])
def process():
    data = request.json
    input_text = data.get("input_text", "")
    gal_code = process_input_data(input_text)
    return jsonify({"gal_code": gal_code})


@app.route("/simulate", methods=["POST"])
def simulate():
    if not request.is_json:
        return make_response(jsonify({"error": "Invalid content type. JSON expected."}), 400)

    data = request.get_json()
    input_text = data.get("input_text", "")
    no_of_branches=int(data.get("no_of_branches",25))


    gal_code = process_input_data(input_text);
    simulator = PetriNetSimulator(gal_code)
    print("pranav special: ",gal_code);

    trace = simulator.simulate(max_steps=no_of_branches)

    response = make_response(jsonify({"trace": trace}), 200)
    response.headers["Content-Type"] = "application/json"
    return response



if __name__ == "__main__":
    app.run(debug=True)