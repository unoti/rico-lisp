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