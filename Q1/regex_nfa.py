operators = {
    "+": 1,
    '.': 2,
    "*": 3,
}
brackets = set(["(", ")"])
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
                try:
                    while stack[-1] != "(":
                        postfix.append(stack.pop())
                except IndexError:
                    raise ValueError("'(' not found when popping")

                stack.pop()
            else:
                stack.append(c)
        else:

            postfix.append(c)

    postfix.extend(token for token in reversed(stack) if token in operators)
    print(postfix)
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
    print("new nfa", c)
    print(nfa)
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
    for lol in n['final_states']:
        nfa['transition_matrix'].append([lol, E, n['start_states'][0]])
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
    nfa['transition_matrix'].append(
        [n1['start_states'][0], E, n2['start_states'][0]])

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
    infix = input()
    print("input: ", infix)
    print()

    while True:
        print(i)
        if len(infix) < 2:
            break
        if infix[i].isalnum() and infix[i+1].isalnum():
            infix = infix[:i+1]+'.'+infix[i+1:]
            print(infix)
        i += 1
        if(i == len(infix)-1):
            break

    postfix = topostfix(infix)
    print("postfix: ", postfix)
    print()
    nfa = nfa(postfix)
    print(nfa)
