

class LispState:
    def __init__(self, old_state = None):
        if old_state:
            self.variables = {**old_state.variables}
        else: 
            self.variables = {**stdlib}

    def execute(self, s_expr):
        function = s_expr[0]
        args = s_expr[1:]

        return self.eval(function)(args, self)

    def eval(self, term):
        if type(term) == str:
            term = self.variables[term]
        elif type(term) == tuple:
            term = self.execute(term)
        return term


def prints(args, state):
    print(" ".join(args))
    return None

def printv(args, state):
    print(state.eval(args[0]))

def setv(args, state):
    state.variables[args[0]] = state.eval(args[1])
def add(args, state):
    return state.eval(args[0]) + state.eval(args[1])

def subtract(args, state):
    return state.eval(args[0]) - state.eval(args[1])

def equal(args, state):
    return state.eval(args[0]) == state.eval(args[1])

def defun(args, state):
    name = args[0]
    inner_args = args[1]
    body = args[2]

    def call(newargs, caller_state):
        inner_state = LispState(old_state=state)
        for name, val in zip(inner_args, newargs):
            inner_state.variables[name] = caller_state.eval(val)
        return inner_state.eval(body)
    state.variables[name] = call

def if_(args, state):
    condition = state.eval(args[0])
    if condition:
        return state.eval(args[1])
    return state.eval(args[2])

def do(args, state):
    for arg in args:
        res = state.eval(arg)
    return res

stdlib = {"+": add, "-": subtract, "=":equal, "defun":defun, "do":do, "if":if_, "prints": prints, "printv":printv, "nil": None, "setv": setv}

state = LispState()

import sys
program_file = open(sys.argv[1]).read()

import re

# This is not a civilized way to write a parser, but it gets the job done.
program_file = re.sub(r"([A-Za-z+_=\-\?]+)", r"'\1',", program_file)
program_file = re.sub(r"([0-9]+)", r"\1,", program_file)
program_file = re.sub("\)", "),", program_file)
program = eval(program_file)

#Now program is a nested tuple of strings and positive integers
state.execute(program)

    
