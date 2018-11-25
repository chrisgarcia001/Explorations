/* Tutorial: https://staff.science.uva.nl/u.endriss/teaching/prolog/prolog.pdf */

last_1([X], X).
last_1([_|Y], Z) :- last_1(Y, Z).

last_2(X, Y) :- append(_, [Y], X).

cons_all(X, [], []).
cons_all(X, [Y|Z], [[X|Y]|A]) :- cons_all(X, Z, A).
         
power([], [[]]).
power([A|B], C) :- 
    power(B, D), cons_all(A, D, E), append(D, E, C).

successor([], [x]).
successor(X, [x|X]).

plus(X, Y, Z) :- append(X, Y, Z).

times(_, [], []).
times([], _, []).
times(X, [Y|Z], A) :- times(X, Z, B), append(X, B, A).

% 3.7
minimum([X], X).
minimum([X|Y], X) :- minimum(Y, Z), X < Z.
minimum([X|Y], Z) :- minimum(Y, Z), X >= Z.

% 3.8
range(X, X, [X]).
range(X, Y, [X|Z]) :- A is X + 1, range(A, Y, Z).

% 3.9
born(jan, date(20,3,1977)).
born(jeroen, date(2,2,1992)).
born(joris, date(17,3,1995)).
born(jelle, date(1,1,2004)).
born(jesus, date(24,12,0)).
born(joop, date(30,4,1989)).
born(jannecke, date(17,3,1993)).
born(jaap, date(16,11,1995)).

year(Y, P) :- born(P, date(_, _, Y)).

before(date(A, B, C), date(D, E, F)) :- C < F.
before(date(A, B, C), date(D, E, F)) :- 
    C = F, B < E.
before(date(A, B, C), date(D, E, F)) :- 
    C = F, B = E, A < D.

older(X, Y) :- born(X, A), born(Y, C), before(A, C).

% 3.11
poly_sum(A, [], A).
poly_sum([], A, A).
poly_sum([(A,B)|C], D, [(E,B)|H]) :-
	select((G,B), D, F),
	E is A + G,
	poly_sum(C, F, H).
poly_sum([(A,B)|C], D, E) :-
	not(member((_,B), D)),
	poly_sum(C, [(A,B)|D], E).
	
	
% 3.14
/* Example: ?- top_solution([v,e,a,d,a,r,a], X). */
% consult(words).
word_letters(W, L) :- atom_chars(W, L).
cover([], _).
cover([A|B], C) :-
    select(A, C, D), cover(B, D).
	
solution(A, W, N) :-
    word(X), word_letters(X, W),
    length(W, N), cover(W, A).

top_solution(L, W, N) :- solution(L, W, N), !.
top_solution(L, W, N) :-
    M is N - 1, M >= 0, top_solution(L, W, M).
top_solution(L, W) :-
    length(L, N), top_solution(L, W, N).
     
	


