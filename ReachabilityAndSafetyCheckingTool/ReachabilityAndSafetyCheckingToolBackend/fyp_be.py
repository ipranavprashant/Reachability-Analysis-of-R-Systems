from flask import Flask, request, jsonify
import itertools
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

if __name__ == "__main__":
    app.run(debug=True)

