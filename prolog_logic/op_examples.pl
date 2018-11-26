/* Algebraic Term Manipulation Examples */

:- op(500, xfy, +).
:- op(400, xfy, *).
:- op(500, xfy, -).
:- op(400, xfy, /).

rw(A+B, 2*A+2*B).

/* Example:. ?- double_all(2+(3*y*z)+(4*x)+(11*x*y), X). */
double_all(A+B, 2*A+C) :- double_all(B,C), !.
double_all(A, 2*A).