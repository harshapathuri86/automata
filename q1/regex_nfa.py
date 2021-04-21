import json
import sys
operators = {
    "+": 1,
    '.': 2,
    "*": 3,
}
brackets = ["(", ")"]
num = 0
stack = []
E = '$'
i = 0


def topostfix(infix):
    stack = []
    postfix = []

    for c in infix:
        if c in operators:

            if stack:
                top = stack[-1]

                while top in operators and operators[top] >= operators[c]:
                    postfix.append(stack.pop())

                    if stack:
                        top = stack[-1]
                    else:
                        break

            stack.append(c)

        elif c in brackets:

            if c == ")":
                while stack[-1] != "(":
                    postfix.append(stack.pop())
                stack.pop()
            else:
                stack.append(c)
        else:
            postfix.append(c)

    postfix.extend(token for token in reversed(stack) if token in operators)
    # print(postfix)
    return postfix


def createNew(c):
    global num
    num += 1
    a = "q0_{}".format(num)
    b = "q1_{}".format(num)
    nfa = {}
    nfa['states'] = [a, b]
    nfa['letters'] = [c]
    nfa["transition_matrix"] = []
    nfa['start_states'] = [a]
    nfa['final_states'] = [b]
    nfa['transition_matrix'].append([a, c, b])
    return nfa


def union(n1, n2, c):
    global num
    num += 1
    a = "q0_{}".format(num)
    b = "q1_{}".format(num)
    nfa = {}
    nfa['states'] = n1['states']+n2['states']
    nfa['states'].append(a)
    lol1 = n1['letters']+n2['letters']
    lol1.append(E)
    nfa['letters'] = list(set(lol1))
    nfa["transition_matrix"] = []
    nfa['start_states'] = [a]
    nfa['final_states'] = n1['final_states']+n2['final_states']
    nfa['transition_matrix'] = n1['transition_matrix']+n2['transition_matrix']
    nfa['transition_matrix'].append([a, E, n1['start_states'][0]])
    nfa['transition_matrix'].append([a, E, n2['start_states'][0]])

    return nfa


def star(n, c):
    global num
    num += 1
    a = "q0_{}".format(num)
    nfa = {}

    nfa['states'] = n['states']
    nfa['states'].append(a)

    lol1 = n['letters']
    lol1.append(E)
    nfa['letters'] = list(set(lol1))

    nfa["transition_matrix"] = []
    nfa['start_states'] = [a]
    nfa['final_states'] = n['final_states']

    nfa['transition_matrix'] = n['transition_matrix']
    for l1 in n['start_states']:
        for l2 in n['final_states']:
            nfa['transition_matrix'].append([l2, E, l1])
        nfa['transition_matrix'].append([nfa['start_states'][0], E, l1])
    nfa['final_states'].append(a)

    return nfa


def concat(n1, n2, c):
    nfa = {}
    nfa['states'] = n1['states']+n2['states']
    lol1 = n1['letters']+n2['letters']
    lol1.append(E)
    nfa['letters'] = list(set(lol1))
    nfa["transition_matrix"] = []
    nfa['start_states'] = n1['start_states']
    nfa['final_states'] = n2['final_states']
    nfa['transition_matrix'] = n1['transition_matrix']+n2['transition_matrix']
    for l1 in n1['final_states']:
        for l2 in n2['start_states']:
            nfa['transition_matrix'].append([l1, E, l2])

    return nfa


def nfa(postfix):
    for c in postfix:
        if c in operators:
            if c == '+':
                n2 = stack.pop()
                n1 = stack.pop()
                new = union(n1, n2, c)
                stack.append(new)
            elif c == '*':
                n1 = stack.pop()
                new = star(n1, c)
                stack.append(new)
            elif c == '.':
                n2 = stack.pop()
                n1 = stack.pop()
                new = concat(n1, n2, c)
                stack.append(new)
        else:
            stack.append(createNew(c))
    return stack.pop()


def main():
    if(len(sys.argv) != 3):
        print("not enough arguments")
        quit()
    with open(sys.argv[1]) as reg:
        infix = json.load(reg)['regex']
    i = 0
    while True:
        if len(infix) < 2:
            break
        if (infix[i].isalnum() and infix[i+1].isalnum()) or (infix[i] == ')' and infix[i+1].isalnum()) or (infix[i].isalnum() and infix[i+1] == '(') or (infix[i] == '*' and infix[i+1].isalnum()) or (infix[i] == '*' and infix[i+1] == '('):
            infix = infix[:i+1]+'.'+infix[i+1:]
            # print(infix)
        i += 1
        if(i == len(infix)-1):
            break
    if infix == "":
        infix = ' '
    postfix = topostfix(infix)
    # print("postfix: ", postfix)
    final = nfa(postfix)
    # print(final)
    if infix == " ":
        final['letters'] = [""]
        for transition in final['transition_matrix']:
            transition[1] = ""
    with open(sys.argv[2], 'w') as output:
        output.write(json.dumps(final, indent=4))


main()
