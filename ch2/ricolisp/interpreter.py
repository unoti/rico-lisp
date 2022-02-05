from typing import List as PythonList
import math
import operator as op

#from .token import Token

Symbol = str              # Symbol is implemented as a Python str
Number = (int, float)     # Number is implemented as either a Python int or float
Atom   = (Symbol, Number) # An Atom is a Symbol or Number
List   = list             # List is implemented as a Python list
Exp    = (Atom, List)     # An expression is either an Atom or List
Env    = dict             # An environment is a mapping of {variable: value}. Dict for now; we'll expand later.

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
    if isinstance(x, Symbol):      # variable reference
        return env[x]
    if isinstance(x, Number):      # constant number
        return x                
    if x[0] == 'if':               # conditional
        (_, test, conseq, alt) = x
        result = eval(test,env)
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    if x[0] == 'define':           # definition
        (_, symbol, exp) = x
        env[symbol] = eval(exp, env)
        return None
    
    # Procedure call.
    proc = eval(x[0], env)
    args = [eval(arg, env) for arg in x[1:]]
    return proc(*args)

def unparse(exp):
    """Convert a Python object back into a lisp parsable string.

    This will for example convert [1,2,3] into '(1,2,3)'.
    """
    if isinstance(exp, List):
        return '(' + ' '.join(map(unparse, exp)) + ')' 
    else:
        return str(exp)

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