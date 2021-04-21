## Q1 - Regex to NFA

- Added concatenation symbol (.) in the given sequence to identify concatenation
- Converted the infix regular expression into postfix expression
- Then evaluated the postfix regular expression using NFAs instead of numbers/letters
- Similar to evaluation of the postfix, when ever I pushed a letter I made an NFA for it. So, when I pop out letters from the stack I get NFAs.
- I merged the NFAs based on the operator found (union/concatenation/star) using different functions for each which returns the merged NFA.
- Finally, we get the final NFA in the stack. 
- I handled the cases where regex is of length less than 2 seperately.

## Q2 - NFA to DFA

- I created a powerset of the states in the NFA as the states of the NFA
- Start state for the DFA is same as that of NFA. So, I just copied the NFA start states to DFA
- I calculated the transition matrix by combining all possible transitions for the substates of DFA states in the NFA and removing duplicates.
- I calculated the final states as the all states of the DFA which consists of the final state of the NFA

## Q3 - DFA to Regex

- First, I creaated the GNFA for the given DFA by adding new start and end states
- Next, for every state in the GNFA which is not either start or end state, I removed it and updated the the transission values of the connected states.
>
    R_ss is the value of the transition from state S to itself
    R_ij is the value of the transition from state Qi   to Qj
    R_sj is the value of the transition from state S to     Qj
    R_is is the value of the transition from state Qi   to S
    Updated value of R_ij = (R_is)(R_ss)*(R_sj)+(Rij)

- I called the function recursively. It returns the GNFA with two states start and end. The transition value between these two states is the value of the Regualar Expressions

## Q4 - Minimize DFA

- First, I removed the unreachable states in the DFA by running DFS from the start state
- I created 2 partitions,  the set of final states and the set of remaining states
- By considering two states Si,Sj in a partition, i checked if they are distinguisable by checking their transitions and if the next states are in the same partition or not.
- I removed the old partition and added a new one for the non distuinguishable states
- A single state is non distuinguishable with itself. So , if there are no other simialr states, a single state forms a partition
- I continied making partitions, till I get same partitions for two consecutive iterations
- I constructed the minimal DFA from the obtained partitions


### [Video](https://iiitaphyd-my.sharepoint.com/:v:/g/personal/harsha_pathuri_students_iiit_ac_in/ERv_Hmka_hFLo3FkixGwR2AB1Ik3eqxy0Tpdqo3_YR7Ffg?e=LD3VnI)

[https://iiitaphyd-my.sharepoint.com/:v:/g/personal/harsha_pathuri_students_iiit_ac_in/ERv_Hmka_hFLo3FkixGwR2AB1Ik3eqxy0Tpdqo3_YR7Ffg?e=LD3VnI](https://iiitaphyd-my.sharepoint.com/:v:/g/personal/harsha_pathuri_students_iiit_ac_in/ERv_Hmka_hFLo3FkixGwR2AB1Ik3eqxy0Tpdqo3_YR7Ffg?e=LD3VnI)
