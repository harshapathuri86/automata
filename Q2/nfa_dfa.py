import json
from itertools import combinations


def power_set(items):
    powerset = [[]]
    for i in items:
        for sub in powerset:
            powerset = powerset+[list(sub)+[i]]
    return powerset


with open('input.json', 'r') as input:
    nfa = json.loads(input.read())


dfa = {}
numstates = 1
for i in range(len(nfa["states"])):
    numstates = numstates*2

dfa['states'] = power_set(nfa['states'])

dfa['letters'] = nfa['letters']

dfa['transition_function'] = []


for states in dfa['states']:
    for inp in nfa['letters']:
        temp = []
        for state in states:
            for func in nfa['transition_function']:
                if state == func[0] and inp == func[1]:
                    temp.append(func[2])
        dfa['transition_function'].append([states, inp, temp])

dfa['start_states'] = nfa['start_states']
dfa['final_states'] = []
for states in dfa['states']:
    for state in states:
        if state in nfa['final_states'] and states not in dfa['final_states']:
            dfa['final_states'].append(states)

with open('output.json', 'w') as outjson:
    outjson.write(json.dumps(dfa, indent=4))
