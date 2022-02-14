Goal of this section is to write an intepreter that can execute this program,
where the program is expressed as a nested Python list.
```py
prg = [
    ['print', 'We love', 'cats and dogs'],
    ['print', ['+', 1, 2]]
]
```

The output of this program should be
```
my name is richard
3
```


Things that become clear at the end of this code:
* **Variables.** We'll need some way to save variables, and to separate variable names from string constants.  We won't want all globals, so we'll want to establish some way to do scoped variables.
* **Functions/procedures**.  We need some way to write functions.
* **Unit Testing.** If we want to be able to refactor this code, we need unit tests so we can iterate more quickly.

At this point let's look at how Lisp works, because it's easy to see how our current approach might not be the most elegant.