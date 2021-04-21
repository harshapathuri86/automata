import json
import sys


def removeUnreachable(dfa):
    newdfa = {}
    newdfa['states'] = []
    newdfa['letters'] = dfa['letters']
    newdfa['transition_matrix'] = []
    newdfa['start_states'] = dfa['start_states']
    newdfa['final_states'] = []
    q = []
    [q.append(state) for state in dfa['start_states']]
    newdfa['states'] += dfa['start_states']
    isreached = []
    while q:
        state = q.pop()
        for start, letter, end in dfa['transition_matrix']:
            if start == state:
                newdfa['transition_matrix'].append([start, letter, end])
                if not end in newdfa['states']:
                    newdfa['states'].append(end)
                    q.append(end)
    for final in dfa['final_states']:
        if final in newdfa['states']:
            newdfa['final_states'].append(final)
    return newdfa


def endStates(state, dfa):
    states = set()
    for start, _, end in dfa['transition_matrix']:
        if start == state:
            states.add(end)
    return list(states)


def sameState(state1, state2, dfa):
    if endStates(state1, dfa) != endStates(state2, dfa):
        return False
    return True


def createNewPartition(partitions, dfa):
    totalPartitions = []
    for partition in partitions:
        newPartitions = []
        isCompared = [0 for state in partition]
        for i, state in enumerate(partition):
            if isCompared[i]:
                continue
            similarStates = []
            for j, nextstate in enumerate(partition[i:]):
                if isCompared[j]:
                    continue
                if sameState(state, nextstate, dfa):
                    isCompared[j] = True
                    similarStates.append(nextstate)
            newPartitions.append(similarStates)
        totalPartitions += newPartitions
    return totalPartitions


def newState(state, partitions):
    for partition in partitions:
        if state in partition:
            return partition
    return []


def merge(partitions, dfa):
    newdfa = {}
    newdfa['states'] = []
    newdfa['letters'] = dfa['letters']
    newdfa['transition_matrix'] = []
    newdfa['start_states'] = []
    newdfa['final_states'] = []

    for partition in partitions:
        for state in partition:
            if state in dfa['final_states']:
                if partition not in newdfa['final_states']:
                    newdfa['final_states'].append(partition)
                if partition not in newdfa['start_states']:
                    newdfa['start_states'].append(partition)
        newdfa['states'].append(partition)

    for start, letter, end in dfa['transition_matrix']:
        transition = [newState(start, partitions), letter,
                      newState(end, partitions)]
        if transition not in newdfa['transition_matrix']:
            newdfa['transition_matrix'].append(transition)
    return newdfa


def main():
    if(len(sys.argv) != 3):
        print("not enough arguments")
        quit()
    with open(sys.argv[1], 'r') as input:
        dfa = json.loads(input.read())
    dfa = removeUnreachable(dfa)
    partitions = []
    partitions.append(dfa['final_states'])
    partitions += [list((set(dfa['states'])-set(dfa['final_states'])))]
    finaldfa = {}
    while True:
        new_partitions = createNewPartition(partitions, dfa)
        if new_partitions == partitions:
            finaldfa = merge(partitions, dfa)
            with open(sys.argv[2], 'w') as output:
                output.write(json.dumps(finaldfa, indent=4))
            break
        partitions = new_partitions


main()
