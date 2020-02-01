# DPLL-SAT-Solver

Davis–Putnam–Logemann–Loveland (DPLL) algorithm is a complete, backtracking-based search algorithm for deciding the satisfiability of propositional logic formulae in conjunctive normal form.

## Run

Input files format follows [DIMACS](http://www.satcompetition.org/2004/format-solvers2004.html).

To run on the benchmarks folder do:
`python3 sat_dpll.py --run_benchmarks`. The code takes around 6 seconds to solve 100 SAT problems.

To run with a seperate input file, just do:
`python3 sat_dpll.py --input_file your_file`

## References

- https://en.wikipedia.org/wiki/DPLL_algorithm
- https://ths.rwth-aachen.de/wp-content/uploads/sites/4/teaching/vorlesung_satchecking/ws14_15/02a_sat_handout.pdf
- http://www.cril.univ-artois.fr/~coste/Articles/coste-etal-sat05.pdf

