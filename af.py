###
#    Class to model an automata
#   initial state, final state, alphaber, transitions
###
class Automata:
    def __init__(self, q, expression, alphabet, q0, f, transitions):
        self.q = q
        self.expression = expression
        self.alphabet = alphabet
        self.q0 = q0
        self.f=f
        self.transitions = transitions

###
#    Class to model an state 
#    the class is used only in direct method 
###
class State:
    def __init__(self, q0, f):
        self.q0 = q0
        self.f = f

