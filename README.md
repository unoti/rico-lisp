# rico-lisp
A simple lisp interpreter in Python.


## Demo
```
> (define make-account
>     (lambda (balance)
>         (lambda (amt)
>             (begin (set! balance (+ balance amt))
>                     balance))))
> (define account1 (make-account 100))
> (account1 -20)
80
> (account1 -20)
60
> (define account2 (make-account 100.00))
> (account2 40)
140
> (account2 -10)
130
> exit
```

## TODO
Expand this so that I can write something like Asteroids.
* [Tail Call Optimization](https://en.wikipedia.org/wiki/Tail_call)
    * To write a simple game I need to iterate infinitely.  This means either TCO, or cheating by implementing an explicit loop structure.
* [Data Structures](https://www.csie.ntu.edu.tw/~course/10420/Resources/lp/node50.html)
    * [Association Lists](https://www.csie.ntu.edu.tw/~course/10420/Resources/lp/node51.html)
* Cleanup/exception handling.
    * To write a game, I need to create graphics structures such as windows which need to be de-allocated if the game halts unexpectedly.
* Stack traces
    * We'll need to be able to report what the interpreter was doing when we, for example, reference a variable that doesn't exist.  To do that we'd probably change the parser to attach properties with each token detailing the file, line number, and character position.