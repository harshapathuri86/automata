import json
import sys
from itertools import combinations


def power_set(items):
    powerset = [[]]
    for i in items:
        for sub in powerset:
            powerset = powerset+[list(sub)+[i]]
    return powerset


def main():
    if(len(sys.argv) != 3):
        print("not enough arguments")
        quit()
    with open(sys.argv[1]) as inp:
        nfa = json.loads(inp.read())

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
                        if func[2] not in temp:
                            temp.append(func[2])
            dfa['transition_function'].append([states, inp, temp])

    dfa['start_states'] = [nfa['start_states']]
    dfa['final_states'] = []
    for states in dfa['states']:
        for state in states:
            if state in nfa['final_states'] and states not in dfa['final_states']:
                dfa['final_states'].append(states)

    with open(sys.argv[2], 'w') as output:
        output.write(json.dumps(dfa, indent=4))


main()
