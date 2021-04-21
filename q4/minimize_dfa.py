import json
import sys


def removeUnreachable(dfa):
    newdfa = {}
    newdfa['states'] = []
    newdfa['letters'] = dfa['letters']
    newdfa['transition_function'] = []
    newdfa['start_states'] = dfa['start_states']
    newdfa['final_states'] = []
    q = []
    [q.append(state) for state in dfa['start_states']]
    newdfa['states'] += dfa['start_states']
    isreached = []
    while q:
        state = q.pop()
        for start, letter, end in dfa['transition_function']:
            if start == state:
                newdfa['transition_function'].append([start, letter, end])
                if not end in newdfa['states']:
                    newdfa['states'].append(end)
                    q.append(end)
    for final in dfa['final_states']:
        if final in newdfa['states']:
            newdfa['final_states'].append(final)
    return newdfa


def endStates(state, letter, dfa, partitions):
    for start, l, end in dfa['transition_function']:
        if start == state and letter == l:
            for i, partition in enumerate(partitions):
                if end in partition:
                    return i
    return None


def sameState(state1, state2, partitions, dfa):
    for letter in dfa['letters']:
        if endStates(state1, letter, dfa, partitions) != endStates(state2, letter, dfa, partitions):
            return False
    return True


def createNewPartition(partitions, dfa):
    totalPartitions = []
    for partition in partitions:
        newPartitions = []
        isSelected = [False for state in partition]
        for i, state in enumerate(partition):
            if isSelected[i]:
                continue
            similarStates = []
            for j, nextstate in enumerate(partition[i:]):
                # print(state, nextstate, partition[i:], len(
                # isSelected), j, isSelected[i+j])
                if isSelected[i+j]:
                    continue
                # print(state, nextstate, sameState(
                    # state, nextstate, partition, dfa))
                if sameState(state, nextstate, partitions, dfa):
                    isSelected[j] = True
                    similarStates.append(nextstate)
            newPartitions.append(similarStates)
        # print(newPartitions)
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
    newdfa['transition_function'] = []
    newdfa['start_states'] = []
    newdfa['final_states'] = []

    for partition in partitions:
        for state in partition:
            if state in dfa['final_states']:
                if partition not in newdfa['final_states']:
                    newdfa['final_states'].append(partition)
            if state in dfa['start_states']:
                if partition not in newdfa['start_states']:
                    newdfa['start_states'].append(partition)
        newdfa['states'].append(partition)

    for start, letter, end in dfa['transition_function']:
        transition = [newState(start, partitions), letter,
                      newState(end, partitions)]
        if transition not in newdfa['transition_function']:
            newdfa['transition_function'].append(transition)
    return newdfa


def main():
    if(len(sys.argv) != 3):
        # print("not enough arguments")
        quit()
    with open(sys.argv[1], 'r') as input:
        dfa = json.loads(input.read())
    dfa = removeUnreachable(dfa)
    # print(dfa)
    partitions = []
    partitions.append(dfa['final_states'])
    partitions += [list((set(dfa['states'])-set(dfa['final_states'])))]
    finaldfa = {}
    # print(partitions)
    while True:
        new_partitions = createNewPartition(partitions, dfa)
        # print(new_partitions)
        if sorted(new_partitions) == sorted(partitions):
            finaldfa = merge(partitions, dfa)
            with open(sys.argv[2], 'w') as output:
                output.write(json.dumps(finaldfa, indent=4))
            break
        partitions = new_partitions


main()
