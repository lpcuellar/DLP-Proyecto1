from tree import *
from transitions import *
from af import *
import collections


OPERATORS = ['.', '|', '*', '(', ')']

def check(dfa, new_state):
    for state in dfa:
        if collections.Counter(state.q0) == collections.Counter(new_state):
            return False
    return True

def select(states, id):
    for state in states:
        if collections.Counter(state.q0) == collections.Counter(id):
            return state
    return False

def important_states(tree):
    nodes = []
    if tree.symbol not in OPERATORS and tree.symbol != "e" and tree.left == None and tree.right == None:
        nodes.append(tree)
    if tree.left != None:
        resp = important_states(tree.left)
        for i in resp:
            nodes.append(i)
    if tree.right != None:
        resp = important_states(tree.right)
        for i in resp:
            nodes.append(i)
    return nodes

def nullable(tree):
    if tree.symbol == "e":
        return True
    elif tree.symbol == ".":
        if nullable(tree.left) and nullable(tree.right):
            return True
    elif tree.symbol == "*":
        return True
    elif tree.symbol == "|":
        if nullable(tree.left) or nullable(tree.right):
            return True
        else:
            return False
    return False

def first_pos(tree):
    pos = []
    if tree.symbol in OPERATORS:
        if tree.symbol == "|":
            temp1 = first_pos(tree.left)
            temp2 = first_pos(tree.right)
            for num in temp1:
                pos.append(num)
            for num in temp2:
                pos.append(num)
        elif tree.symbol == "*":
            temp1 = first_pos(tree.left)
            for num in temp1:
                pos.append(num)
        elif tree.symbol == ".":
            temp1 = first_pos(tree.left)
            for num in temp1:
                pos.append(num)
            if nullable(tree.left):
                temp2 = first_pos(tree.right)
                for num in temp2:
                    pos.append(num)
       
    elif tree.symbol != "e":
        pos.append(tree)
    return pos

def last_pos(tree):
    pos = []
    if tree.symbol in OPERATORS:
        if tree.symbol == "|":
            temp1 = last_pos(tree.left)
            temp2 = last_pos(tree.right)
            for num in temp1:
                pos.append(num)
            for num in temp2:
                pos.append(num)
        elif tree.symbol == "*":
            temp1 = last_pos(tree.left)
            for num in temp1:
                pos.append(num)
        elif tree.symbol == ".":
            temp1 = last_pos(tree.right)
            if nullable(tree.right):
                temp2 = last_pos(tree.left)
                for num in temp2:
                    pos.append(num)
            for num in temp1:
                pos.append(num)
        
    elif tree.symbol != "e":
        pos.append(tree)
    return pos


def followpos(tree, table):
    if tree.symbol == ".":
        temp1 = last_pos(tree.left)
        temp2 = first_pos(tree.right)
        for i in temp1:
            for num in temp2:
                table[i].append(num)
    elif tree.symbol == "*":
        temp1 = last_pos(tree)
        temp2 = first_pos(tree)
        for i in temp1:
            for num in temp2:
                table[i].append(num)
    elif tree.symbol == "+":
        temp1 = last_pos(tree.left)
        temp2 = first_pos(tree.left)
        for i in temp1:
            for num in temp2:
                table[i].append(num)

    if tree.left != None:
        followpos(tree.left, table)
    if tree.right != None:
        followpos(tree.right, table)

def direct_const(tree, exp):
    new_tree = Tree()
    new_tree.symbol = "."
    right_t = Tree()
    right_t.symbol = "#"
    new_tree.right = right_t
    new_tree.left = tree

    states_eval = important_states(new_tree)
    first = first_pos(new_tree)
    last = last_pos(new_tree)
    table = {}
    for pos in states_eval:
        table[pos] = []

    followpos(new_tree, table)
    inicial = first_pos(new_tree)
    final = last_pos(new_tree)
    print("First pos for directed")
    print("[")
    for tree in inicial: 
        print(str(tree.symbol) + ',') 
    print("]")

    print("Last pos for directed")
    for tree in final:
        print(str(tree.symbol) + "," )
    print("Table generated for direct method")
    for key in table:
        x = "["
        key_string = str(key.symbol)
        for tree in table[key]:
            y = (str(tree.symbol) + ",")
            x += y
        x += "]"
        print(key_string, ":", x)

    auto_direct = create(inicial, final, table, exp)

    return auto_direct

def create(inicial, final, table, exp):
    first = State(inicial, 0)
    dfa_transitions = []
    dfa_states = [] 
    dfa_states.append(first)
    acceptance_states = []
    if final[-1] in first.q0:
        acceptance_states.append(first.f)

    symbols = []
    for symbol in exp:
        if symbol not in OPERATORS and symbol not in symbols and symbol != "e":
            symbols.append(symbol)
    
    print("Alphabet for directed")
    print(symbols)
    
    for state in dfa_states:
        for symbol in symbols:
            temp = []
            for pos in state.q0:
                if pos.symbol == symbol:
                    tos = table[pos]
                    for t in tos:
                        if t not in temp:
                            temp.append(t)
            if check(dfa_states, temp) and temp != []:
                print("creating new state and new transition of dfa")
                new_state = State(temp, len(dfa_states))
                print("State generated")
                print(new_state.q0, new_state.f)
                if final[-1] in temp:
                    print(new_state.f)
                    acceptance_states.append(new_state.f)
                 
                dfa_states.append(new_state)
                transition1 = Transition(start=state.f,transition=symbol,end=dfa_states[-1].f)
                dfa_transitions.append(transition1)
            elif temp != []:
                selected = select(dfa_states, temp)
                if selected:
                    print("just adding a new transition to dfa")
                    transition2 = Transition(start=state.f, transition=symbol, end=selected.f)
                    dfa_transitions.append(transition2)
    
    print("Transitions of dfa generated")
    for transition in dfa_transitions:
        print('('+str(transition.start)+', '+transition.transition+', '+str(transition.end)+'), ') 
    
    print(acceptance_states)
    afd_direct = Automata(dfa_states,"eval",symbols,None,acceptance_states,dfa_transitions)
    return afd_direct
