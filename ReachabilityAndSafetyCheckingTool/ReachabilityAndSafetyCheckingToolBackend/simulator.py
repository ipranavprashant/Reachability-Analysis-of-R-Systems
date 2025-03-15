# import random
# import copy

# class PetriNetSimulator:
#     def __init__(self, gal_code):
#         self.variables = {}  # Initial variable states
#         self.transitions = {}  # Transition name -> (guard, actions)
#         self._parse_gal_code(gal_code)

#     def _parse_gal_code(self, gal_code):
#         lines = gal_code.strip().splitlines()
#         current_transition = None

#         for line in lines:
#             line = line.strip()
#             if not line:
#                 continue
                
#             if line.startswith("int"):
#                 # Parse variable declaration
#                 var, val = line.replace(";", "").split("=")
#                 var_name = var.split()[1].strip()
#                 self.variables[var_name] = int(val.strip())

#             elif line.startswith("transition"):
#                 # Parse transition header
#                 name = line.split("transition")[1].split("[")[0].strip()
#                 guard = line.split("[")[1].split("]")[0].strip()
#                 current_transition = name
#                 self.transitions[name] = (guard, [])

#             elif current_transition and ";" in line:
#                 # Parse actions
#                 actions = []
#                 for action in line.split(";"):
#                     action = action.strip()
#                     if action:  # Skip empty strings
#                         actions.append(action)
#                 self.transitions[current_transition] = (self.transitions[current_transition][0], actions)

#     def _evaluate_guard(self, guard, marking):
#         # Simple case
#         if guard.lower() == "true":
#             return True
            
#         # Split into individual conditions
#         for condition in guard.split("&&"):
#             condition = condition.strip()
            
#             # Check for each operator explicitly
#             # Important: Check longer operators first (>= before >)
#             if ">=" in condition:
#                 var, val = condition.split(">=")
#                 var, val = var.strip(), val.strip()
#                 if marking.get(var, 0) < int(val):
#                     return False
#             elif "<=" in condition:
#                 var, val = condition.split("<=")
#                 var, val = var.strip(), val.strip()
#                 if marking.get(var, 0) > int(val):
#                     return False
#             elif "==" in condition:
#                 var, val = condition.split("==")
#                 var, val = var.strip(), val.strip()
#                 if marking.get(var, 0) != int(val):
#                     return False
#             elif "!=" in condition:
#                 var, val = condition.split("!=")
#                 var, val = var.strip(), val.strip()
#                 if marking.get(var, 0) == int(val):
#                     return False
#             elif ">" in condition:  # Check AFTER >=
#                 var, val = condition.split(">")
#                 var, val = var.strip(), val.strip()
#                 if marking.get(var, 0) <= int(val):  # Not strictly greater
#                     return False
#             elif "<" in condition:  # Check AFTER <=
#                 var, val = condition.split("<")
#                 var, val = var.strip(), val.strip()
#                 if marking.get(var, 0) >= int(val):  # Not strictly less
#                     return False
                    
#         # All conditions passed
#         return True

#     def _apply_actions(self, actions, marking):
#         result = copy.deepcopy(marking)
        
#         for action in actions:
#             if "+=" in action:
#                 var, val = action.split("+=")
#                 var, val = var.strip(), val.strip()
#                 result[var] = result.get(var, 0) + int(val)
#             elif "-=" in action:
#                 var, val = action.split("-=")
#                 var, val = var.strip(), val.strip()
#                 result[var] = result.get(var, 0) - int(val)
                
#         return result

#     def _get_fireable_transitions(self, marking):
#         fireable = []
        
#         for name, (guard, actions) in self.transitions.items():
#             # First check if guard is satisfied
#             if self._evaluate_guard(guard, marking):
#                 # Then check if resulting marking would be valid (no negative places)
#                 new_marking = self._apply_actions(actions, marking)
#                 if all(v >= 0 for v in new_marking.values()):
#                     fireable.append((name, new_marking))
        
#         return fireable

#     def simulate(self, max_steps=100):
#         current = copy.deepcopy(self.variables)
#         trace = [("initial", copy.deepcopy(current))]
        
#         for _ in range(max_steps):
#             fireable = self._get_fireable_transitions(current)
            
#             if not fireable:
#                 break
                
#             # Select a random transition from those that are fireable
#             transition_name, next_marking = random.choice(fireable)
#             trace.append((transition_name, copy.deepcopy(next_marking)))
#             current = next_marking
            
#         return trace



import random
import copy

class PetriNetSimulator:
    def __init__(self, gal_code):
        self.variables = {}  # Initial variable states
        self.transitions = {}  # Transition name -> (guard, actions)
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
                # Parse variable declaration
                var, val = line.replace(";", "").split("=")
                var_name = var.split()[1].strip()
                self.variables[var_name] = int(val.strip())
                print(f"Declared variable: {var_name} = {self.variables[var_name]}")

            elif line.startswith("transition"):
                # Parse transition header
                name = line.split("transition")[1].split("[")[0].strip()
                guard = line.split("[")[1].split("]")[0].strip()
                current_transition = name
                self.transitions[name] = (guard, [])
                print(f"\nFound transition: {name} with guard: '{guard}'")

            elif current_transition and ";" in line:
                # Parse actions
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




        

   
