# introAI

## Backtracking search

Backtracking Search is a recursive algorithm used to find a valid solution to a constraint satisfaction problem (CSP). It systematically explores the search space by trying different variable assignments and checks if they satisfy all constraints. If an assignment violates a constraint, the algorithm backtracks, undoing the last assignment, and tries a new one. This approach ensures that the search process covers all possibilities, while pruning invalid solutions early on.

Backtracking is efficient in finding solutions but can be improved by using heuristics such as:

Select-Unassigned-Variable (SAV): Chooses the next variable to assign.
Order-Domain-Values (ODV): Orders the domain values to minimize conflicts.

## AC-3 algorithm 

AC-3 (Arc Consistency 3) is an algorithm used to preprocess a CSP by enforcing arc consistency before or during search. The goal of AC-3 is to reduce the domain of variables by removing values that are inconsistent with their neighboring variables. For each variable, it checks if there exists at least one valid value in its neighbors' domains that satisfies the binary constraint. If no such value exists, it removes the inconsistent value from the domain. This pruning of domains often simplifies the problem, making the subsequent search more efficient.

Incorporating AC-3 before Backtracking Search reduces the overall search space, leading to faster solutions for many CSPs.
