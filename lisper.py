program = (
        "do", 
        ("prints", "try doubling function"),
        ("defun", "double", ("x",), ("+", "x", "x")), 
        ("printv", ("double", 1)),
        (
            "defun", "multiply_inner", ("x", "y", "acc"), 
            (
                "if", 
                ("=", "y", 0),
                "acc",
                ("multiply_inner", "x", ("-", "y", 1), ("+", "acc", "x"))
            )
        ),
        (
            "defun", "multiply", ("x", "y"), ("multiply_inner", "x", "y", 0)
        ), 
        ("prints", "try multiplication"),
        ("printv",  ("multiply", 6, 7)),
        ("prints", "To demonstrate the power of this subset, we define ML style lists"),
        ("prints", "A list is a function that returns its nth element, or nil if it is length n"),
        (
            "defun", "list", ("head", "body"), 
            (
                "do",
                (
                    "defun", "returned_list", ("index",),
                    (
                        "if",
                        ( "=", "index", 0),
                        "head",
                        ("body", ("-", "index", 1))
                    )
                ),
                "returned_list"
                
            )
        ),
        (
            "defun", "tail", ("the_list",),
            (
                "do",
                (
                    "defun", "returned_tail", ("index",),
                    ("the_list", ("+", "index", 1)),
                ),
                ( 
                    "if",
                    ("=", ("returned_tail", 0), "nil"),
                    ("setv", "returned_tail", "nil"),
                    "nil"
                ),
                "returned_tail"
            )
        ),
        ("defun", "retnil", ("index",), "nil"),
        (
            "defun", "startlist", ("head",),
            ("list", "head", "retnil")
        ),
        ("prints", "list defined"),
        ("setv", "mylist", ("list", 5, ("list", 6, ("startlist", 7)))),
        ("prints", "try printing list values"),
        ("printv", ("mylist", 0)),
        ("printv", ("mylist", 1)),
        ("printv", ("mylist", 2)),
        ("prints", "try tail function"),
        ("printv", (("tail", "mylist"), 0)),
        ("prints", "can we print a list?"),
        (
            "defun", "print_list", ("a_list",),
            (
                "if", ("=", "a_list", "nil"),
                "nil",
                (
                    "do", 
                    ("printv", ("a_list", 0)),
                    ("print_list", ("tail", "a_list"))
                )
            )
        ),
        ("print_list", "mylist"),
        ("prints", "Can we reverse a list?"),
        (
                "defun", "put_end", ("the_list", "value"),
                (
                    "if",
                    ("=", "the_list", "nil"),
                    ("startlist", "value"),
                    ("list", ("the_list", 0), ("put_end", ("tail", "the_list"), "value"))
                )
        ),
        ("setv", "list_end_8", ("put_end", "mylist", 8)),
        ("setv", "list_end_9", ("put_end", "list_end_8", 9)),
        ("prints", "Try adding elements to end"),
        ("print_list", "list_end_9"),
        (
            "defun", "reverse_list", ("the_list",),
            (
                "if",
                ("=", "the_list", "nil"),
                "nil",
                ("put_end", ("reverse_list", ("tail", "the_list")), ("the_list", 0))
            )
        ),
        ("prints", "reverse list and print it"),
        ("setv", "reversed_list", ("reverse_list", "list_end_9")),
        ("print_list", "reversed_list"),
)


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
    print(args[0])
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

state.execute(program)

    
