import re
from transitions import *
from af import *

#method from https://www.geeksforgeeks.org/python-get-unique-values-list/
def unique(alphabet):
    # insert the list to the set
    list_set = set(alphabet)
    # convert the set to the list
    unique_list = (list(list_set))
    return unique_list

###
#    Thompson algorithm to generate an nfa, it constructs the nfa with clases of automatas with 
#    initial state, final state, transitions and symbols.
#    @params expression to evaluate in postfix
#    @return nfa 
###

def thompson_alg(postfix):
    stack = []
    counter = 0

    for c in postfix:
        if (c != '(') and (c != ')')  and (c != '*') and (c != '|') and (c != '.'):
            #if the character to evaluate is not an operator we make a single transitions 
            #the transitions consist of two initial states and in the label the symbol we 
            #are evaluating 
            state1 = str(counter)
            state2 = str(counter+1)
            states = [state1, state2]
            counter+=2
            transition = Transition(start=state1, transition=c, end=state2)
            transitions = [transition]
            element = Automata(q=states, expression=c, alphabet=[c], q0=state1, f=state2, transitions=transitions)
            stack.append(element)
        else:
            if (c == '|'):
                #if the character to evaluate is the operator or we make the transitions epsilon
                #with the states of the last two elementos

                element2=stack.pop()
                element1=stack.pop()
                initial_state = str(counter)
                final_state = str(counter+1)
                counter+=2
                transition1 = Transition(start=initial_state, transition='e', end=element1.q0)
                transition2 = Transition(start=initial_state, transition='e', end=element2.q0)
                transition3 = Transition(start=element1.f, transition='e', end=final_state)
                transition4 = Transition(start=element2.f, transition='e', end=final_state)

                old_transitions = element1.transitions + element2.transitions
                new_transitions = [transition1, transition2, transition3, transition4]
                current_transitions = old_transitions + new_transitions

                old_states = element1.q + element2.q
                new_states = [initial_state, final_state]
                current_states = old_states + new_states

                current_expression = '(' + element1.expression + '|' + element2.expression + ')'
                current_alphabet = element1.alphabet + element2.alphabet

                element = Automata(q=current_states, expression=current_expression, alphabet=current_alphabet, q0=initial_state, f=final_state, transitions=current_transitions)
                stack.append(element)


            if (c == '.'):
                #if the character to evaluate is the operator . we make the transitions epsilon
                #with the states of the last two elementos
                element2=stack.pop()
                element1=stack.pop()

                new_transitions = []
                element2_transitions = []
                
                for transition in element2.transitions:
                    if transition.start == element2.q0:
                        transition1 = Transition(start=element1.f, transition=transition.transition, end=transition.end)
                        new_transitions.append(transition1)
                    else:
                        element2_transitions.append(transition)    


                old_transitions = element1.transitions + element2_transitions
                current_transitions = old_transitions + new_transitions

                old_states = element1.q + element2.q
                current_states = []

                for state in old_states:
                    if state != element2.q0:
                        current_states.append(state)

                current_expression = '(' + element1.expression + '.' + element2.expression + ')'
                current_alphabet = element1.alphabet + element2.alphabet        

                element = Automata(q=current_states, expression=current_expression, alphabet=current_alphabet, q0=element1.q0, f=element2.f, transitions=current_transitions)
                stack.append(element)

            if (c == '*'):
                #if the character to evaluate is the operator kleen we make the transitions epsilon
                #with the states of the last two elementos
                element = stack.pop()
                initial_state = str(counter)
                final_state = str(counter+1)
                counter+=2
                transition1 = Transition(start=initial_state, transition='e', end=element.q0)
                transition2 = Transition(start=element.f, transition='e', end=final_state)
                transition3 = Transition(start=initial_state, transition='e', end=final_state)
                transition4 = Transition(start=element.f, transition='e', end=element.q0)

                old_transitions = element.transitions 
                new_transitions = [transition1, transition2, transition3, transition4]
                current_transitions = old_transitions + new_transitions

                old_states = element.q 
                new_states = [initial_state, final_state]
                current_states = old_states + new_states

                current_expression = '(' + element.expression + ')*'
                current_alphabet = element.alphabet

                element = Automata(q=current_states, expression=current_expression, alphabet=current_alphabet, q0=initial_state, f=final_state, transitions=current_transitions)
                stack.append(element)
    
    #the last element in the stack is the final automata with all the "mini automatas" together

    last = stack.pop()
    for state in last.q: 
        print(state + ', ') 

    last.alphabet = unique(last.alphabet)
    for char in last.alphabet:
        print(char + ', ')    

    for transition in last.transitions:
        print('('+transition.start+', '+transition.transition+', '+transition.end+'), ') 
    return (last)