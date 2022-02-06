from pydoc import doc
from typing import List as PythonList
import math
import operator as op

#from .token import Token

Symbol = str              # Symbol is implemented as a Python str
Number = (int, float)     # Number is implemented as either a Python int or float
Atom   = (Symbol, Number) # An Atom is a Symbol or Number
List   = list             # List is implemented as a Python list
Exp    = (Atom, List)     # An expression is either an Atom or List

diagnostic_trace = False
#diagnostic_trace = True

def tokenize(chars: str):
    """Convert a string of characters into a list of tokens."""
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()

def atom(token: str) -> Atom:
    """Create an atom from a string.

    Numbers remain numbers; every other token becomes a symbol.
    """
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)

def read_from_tokens(tokens: PythonList) -> Exp:
    """Read an expression from a sequence of tokens."""
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')
    
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    
    if token == ')':
        raise SyntaxError('unexpected )')
        
    return atom(token)

def parse(program: str) -> Exp:
    """Read a string and turn it into an Expression."""
    return read_from_tokens(tokenize(program))


class Env(dict):
    """
    An environment contains variable definitions, and may be linked to a parent environment.
    You can think of it as a dictionary with an optional parent dictionary.
    """
    def __init__(self, parms=(), args=(), outer: 'Env'=None):
        """
        @param parms: Variable names to bind arguments to.
        @param args: Values to bind the variable names to.
        @param outer: A parent environment (optional).  If specified, then we will search
        the parent environments recursively if we cannot find a given value in the current environment.
        """
        self.update(zip(parms, args))
        self.outer = outer
    
    def find(self, var: str) -> 'Env':
        """
        Finds the innermost Env where the given name appears.
        @param var: The name of the variable we're looking for.
        @returns Env: The environment in which this name appears.
        """
        if var in self:
            return self
        if self.outer:
            return self.outer.find(var)
        raise Exception(f'Variable "{var}" not found')


def standard_env() -> Env:
    """Create the standard top-level environment (variable namespace) with some Scheme standard procedures."""
    env = Env()
    env.update(vars(math)) # sin, cos, sqrt, pi, ...
    env.update({
        '+':op.add, '-':op.sub, '*':op.mul, '/':op.truediv, 
        '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '=':op.eq, 
        'abs':     abs,
        'append':  op.add,  
        'apply':   lambda proc, args: proc(*args),
        'begin':   lambda *x: x[-1],
        'car':     lambda x: x[0],
        'cdr':     lambda x: x[1:], 
        'cons':    lambda x,y: [x] + y,
        'eq?':     op.is_, 
        'expt':    pow,
        'equal?':  op.eq, 
        'length':  len, 
        'list':    lambda *x: List(x), 
        'list?':   lambda x: isinstance(x, List), 
        'map':     map,
        'max':     max,
        'min':     min,
        'not':     op.not_,
        'null?':   lambda x: x == [], 
        'number?': lambda x: isinstance(x, Number),  
        'print':   print,
        'procedure?': callable,
        'round':   round,
        'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env

def eval(x: Exp, env: Env) -> Exp:
    """
    Evaluate an expression in an environment.
    """
    if diagnostic_trace:
        print(f'--eval Exp: ', x)
    if isinstance(x, Symbol):        # variable reference
        return env.find(x)[x]

    if not isinstance(x, List):      # constant number
        return x
    
    op, *args = x
    if op == 'quote':              # Quote an expression without evaluating it
        return args[0]
    
    if op == 'if':               # conditional
        (test, conseq, alt) = args
        result = eval(test,env)
        if result:
            exp = conseq
        else:
            exp = alt
        return eval(exp, env)

    if op == 'define':           # definition
        (symbol, exp) = args
        env[symbol] = eval(exp, env)
        return None

    if op == 'set!':             # assignment
        (symbol, exp) = args
        value = eval(exp, env)
        env.find(symbol)[symbol] = value
        return None
    
    if op == 'lambda':           # procedure
        (parms, body) = args
        return Procedure(parms, body, env)
    
    if op == 'while':
        (cond, statement) = args
        result = None
        while True:
            conditional_result = eval(cond, env)
            if not conditional_result:
                break
            result = eval(statement, env)
        return result
        
    # Procedure call.
    proc = eval(x[0], env)
    args = [eval(arg, env) for arg in x[1:]]
    if diagnostic_trace:
        print(f'procedure {x[0]} call with {len(args)} args: ', args)
    return proc(*args)

def unparse(exp):
    """Convert a Python object back into a lisp parsable string.

    This will for example convert [1,2,3] into '(1,2,3)'.
    """
    if isinstance(exp, List):
        return '(' + ' '.join(map(unparse, exp)) + ')' 
    else:
        return str(exp)


class Procedure:
    """A user-defined procedure with variable name bindings.
    """
    def __init__(self, parms, body, env):
        """
        @param pams: A sequence of names that will be used in the procedure.
        @param body: Parsed code forming the body of this procedure.
        @param env: The environment (closure) this procedure runs in.
        """
        self.parms = parms
        self.body = body
        self.env = env
    
    def __call__(self, *args):
        # Create an environment with bindings for this one invocation.
        env = Env(self.parms, args, self.env)
        return eval(self.body, env)   

class Console:
    """A terminal to read input and print things.

    Make your own implementation of the public methods here to make a repl work with other kinds of devices.
    """
    def input(self, prompt: str):
        """Display a prompt to the console and await input."""
        return input(prompt)
    
    def print(self, value):
        """Print output to the console."""
        if value is not None:
            print(unparse(value))

stdio_console = Console() # Singleton for the console attached to stdio.

class LispInterpreter:
    def __init__(self):
        self.env = standard_env() # The top-level global environment for this interpreter.

    def run(self, source_code: str):
        """
        Parse some code, execute it, and return the result.
        """
        expression = parse(source_code)
        return eval(expression, self.env)
    
    def repl(self, prompt:str = '> ', console: Console = stdio_console):
        """Start a read-eval-print loop with the given console device."""
        while True:
            text = console.input(prompt)
            #*TODO: let's instead introduce the concept of EOF into the Console class, and put this 'exit' nonsense in there.
            # The 'exit' thing was just so I could run the repl in a Jupyter notebook.
            if text == 'exit':
                break
            val = self.run(text)
            console.print(val)

if __name__ == '__main__':
    lisp = LispInterpreter()
    lisp.repl()