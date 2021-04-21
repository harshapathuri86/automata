import json
import sys

E = "$"
N = "#"
start = "Q_start"
end = "Q_end"


def convertGnfa(dfa):
    gnfa = {}

    gnfa['states'] = dfa['states']
    gnfa['states'].append(start)
    gnfa['states'].append(end)

    lol1 = dfa['letters']
    lol1.append(E)
    gnfa['letters'] = list(set(lol1))

    gnfa["transition_function"] = []
    gnfa['start_states'] = [start]
    gnfa['final_states'] = [end]

    gnfa['transition_function'] = dfa['transition_function']
    for st in dfa['start_states']:
        gnfa['transition_function'].append([start, E, st])

    for en in dfa['final_states']:
        gnfa['transition_function'].append([en, E, end])

    return gnfa


def update(R_is, R_ss, R_sj, R_ij):
    val = ''
    if R_is == []:
        val += ''
    else:
        a = [str(i) for i in R_is]
        a = '+'.join(a)
        if a != '':
            val += '('+a+')'
        else:
            val += ''
    print(type(R_is))
    # R_is = '('+str(R_is)+')'

    if R_ss == []:
        val += ''
    else:
        a = [str(i) for i in R_ss]
        a = '+'.join(a)
        if a != '':
            val += '('+a+')*'
        else:
            val += ''
    print(type(R_ss))

    if R_sj == []:
        val += ''
    else:
        a = [str(i) for i in R_sj]
        a = '+'.join(a)
        if a != '':
            val += '('+a+')'
        else:
            val += ''
    print(type(R_sj))

    if R_ij != '':
        if R_sj != '':
            val += '+'+str(R_ij)
    else:
        val += ''
    return val


def minimize(gnfa):
    removeS = None
    removeT = None
    R_ss = []

    if len(gnfa['states']) == 2:
        print("min")
        print(gnfa)
        print()
        return gnfa

    for ind, st in enumerate(gnfa['states']):
        if st in [start, end]:
            continue
        removeS = ind
        break

    for i, transition in enumerate(gnfa['transition_function']):
        if transition[0] == gnfa['states'][removeS] and transition[2] == gnfa['states'][removeS]:
            if(transition[0] == 'Q1'):
                print(gnfa['transition_function'])
            R_ss.append(transition[1])
            print("BBBBBBBB", transition)
    gnfa['transition_function'] = [i for i in gnfa['transition_function'] if not (
        i[0] == gnfa['states'][removeS] and i[2] == gnfa['states'][removeS])]

    for q1 in gnfa['states']:
        if q1 == end or q1 == gnfa['states'][removeS]:
            continue
        R_is = []

        for i, transition in enumerate(gnfa['transition_function']):
            if q1 == transition[0] and gnfa['states'][removeS] == transition[2]:
                R_is.append(transition[1])
        gnfa['transition_function'] = [i for i in gnfa['transition_function']
                                       if not (i[0] == q1 and i[2] == gnfa['states'][removeS])]

        for q2 in gnfa['states']:
            if q2 == start or q2 == gnfa['states'][removeS]:
                continue
            print("Q1,Q2", q1, q2, gnfa['states'][removeS])
            R_sj = []
            R_ij = []
            ind = []
            boom = gnfa['transition_function']
            for i, transition in enumerate(gnfa['transition_function']):
                if gnfa['states'][removeS] == transition[0] and q2 == transition[2]:
                    R_sj.append(transition[1])
                    gnfa['transition_function'].remove(transition)
            gnfa['transition_function'] = [i for i in gnfa['transition_function'] if not (
                i[2] == q2 and i[0] == gnfa['states'][removeS])]

            for i, transition in enumerate(gnfa['transition_function']):
                if q1 == transition[0] and q2 == transition[2]:
                    R_ij.append(transition[1])
                    ind.append(i)

            if ind != []:
                index = 0
                for i in ind:
                    gnfa['transition_function'][i][1] = update(
                        R_is, R_ss, R_sj, str(R_ij[index]))
                    index += 1
            else:
                gnfa['transition_function'].append(
                    [q1, update(R_is, R_ss, R_sj, ''), q2])

    gnfa['states'].remove(gnfa['states'][removeS])
    return minimize(gnfa)


def main():
    if(len(sys.argv) != 3):
        print("not enough arguments")
        quit()
    with open(sys.argv[1], 'r') as inpdfa:
        dfa = json.loads(inpdfa.read())

    regex = {}
    regex["regex"] = ""
    gnfa = convertGnfa(dfa)
    gnfa = minimize(gnfa)
    regex['regex'] = gnfa['transition_function'][0][1]

    with open(sys.argv[2], 'w') as output:
        output.write(json.dumps(regex, indent=4))


main()
