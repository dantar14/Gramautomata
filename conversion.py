import re
from typing import Dict, Any, Set, Tuple
def get_reachable_states(nfa: Dict[str, Any], state: Set[Any], alphabet: Set[str]) -> Set[Any]:
    reachable_states = set(state)
    queue = list(state)
    while queue:
        current_state = queue.pop(0)
        for symbol in alphabet:
            for next_state in nfa['transitions'].get((current_state, symbol), set()):
                if next_state not in reachable_states:
                    reachable_states.add(next_state)
                    queue.append(next_state)
    return reachable_states
def nfa_to_dfa(nfa: Dict[str, Any]) -> Dict[str, Any]:
    alphabet = nfa['alphabet']
    initial_state = frozenset(get_reachable_states(nfa, nfa['initial'], alphabet))
    reachable_states = {initial_state}
    queue = [initial_state]
    while queue:
        state = queue.pop(0)
        for symbol in alphabet:
            next_states = set()
            for s in state:
                next_states.update(nfa['transitions'].get((s, symbol), set()))
            next_state = frozenset(get_reachable_states(nfa, next_states, alphabet))
            if next_state not in reachable_states:
                reachable_states.add(next_state)
                queue.append(next_state)
    dfa = {}
    dfa['alphabet'] = alphabet
    dfa['states'] = []
    dfa['initial'] = initial_state
    dfa['transitions'] = {}
    dfa['final'] = set()
    for state in reachable_states:
        dfa['states'].append(state)
        if any(s in nfa['final'] for s in state):
            dfa['final'].add(state)
        for symbol in alphabet:
            next_states = set()
            for s in state:
                next_states.update(nfa['transitions'].get((s, symbol), set()))
            next_state = frozenset(get_reachable_states(nfa, next_states, alphabet))
            if (state, symbol) not in dfa['transitions']:
                dfa['transitions'][state, symbol] = next_state
    final_states = set()
    for state in dfa['states']:
        if any(s in nfa['final'] for s in state):
            final_states.add(state)
    dfa['final'] = final_states
    initial_state = set()
    for s in dfa['initial']:
        initial_state.add(s)
    dfa['initial'] = initial_state
    return dfa
filename = input("Ingrese el nombre del archivo que contiene la definición del AFN: ")
with open(filename, 'r') as f:
    nfa_lines = f.readlines()
nfa = {}
nfa['alphabet'] = set(nfa_lines[3].strip()[3:].split(','))
nfa['states'] = set(range(int(nfa_lines[0].strip())))
nfa['initial'] = set()
nfa['transitions'] = {}
nfa['final'] = set()
state = set()
for line in nfa_lines[4:]:
    match = re.match(r'^(\d+)\s*>', line)
    if not match:
        if line.startswith('f'):
            nfa['final'].add(frozenset({int(line[1:])}))
        continue
    state_id = int(match.group(1))
    state = frozenset({state_id})
    nfa['states'].add(state)
    if state not in nfa['transitions']:
        nfa['transitions'][state] = {}
    for trans in line[match.end():].split('|'):
        parts = trans.strip().split()
        if len(parts) < 3:
            continue
        symbol, dest = parts[1], int(parts[2])
        if symbol not in nfa['transitions'][state]:
            nfa['transitions'][state][symbol] = set()
        nfa['transitions'][state][symbol].add(dest)
dfa = nfa_to_dfa(nfa)
print("El AFN dado es:")
print(f"Alfabeto: {nfa['alphabet']}")
print(f"Estados: {nfa['states']}")
print(f"Estado inicial: {nfa['initial']}")
print(f"Transiciones: {nfa['transitions']}")
print(f"Estados finales: {nfa['final']}")
print("El DFA equivalente es:")
print(f"Alfabeto: {dfa['alphabet']}")
print(f"Estados: {dfa['states']}")
print(f"Estado inicial: {dfa['initial']}")
print(f"Transiciones: {dfa['transitions']}")
print(f"Estados finales: {dfa['final']}") 