from typing import List
def main1():
    prg = [['+', 3, 4]]
    result = run(prg)
    print(f'Program ended. Result={result}')

def main2():   
    prg = [ 
        ['print', 'We love', 'cats and dogs'],
        ['print', ['+', 1, 2]]
    ]
    run(prg)

def run(expressions: List):
    """Run a sequence of commands, or evaluate a sequence of expressions."""
    result = None
    for expression in expressions:
        result = eval(expression)
    return result

def eval(x):
    if not isinstance(x, list):      # constant number or string
        return x
    operator = x[0]
    rest = x[1:]

    if operator == 'print':
        # Initial version:
        # for item in rest:
        #   print(item)
        items = [str(eval(item)) for item in rest]
        output = ' '.join(items)
        print(output)
        return
    
    if operator == '+':
        return rest[0] + rest[1]

    raise Exception(f'Unknown operator {operator}')

if __name__ == '__main__':
    #main1()
    main2()
