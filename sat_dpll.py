import sys
from collections import defaultdict
import os
import time

def parse_dimacs(filename):
	clauses = []
	with open(filename, 'r') as input_file:
		for line in input_file:
			if line[0] in ['c', 'p']:
				continue
			literals = list(map(int, line.split()))
			assert literals[-1] == 0
			literals = literals[:-1]
			clauses.append(literals)
	return clauses

# Jersolow-Wang method
def jersolow_wang_method(cnf):
	literal_weight = defaultdict(int)
	for clause in cnf:
		for literal in clause:
			literal_weight[literal] += 2 ** -len(clause)
	return max(literal_weight, key=literal_weight.get)

# Jersolow-Wang 2-sided method (consider only positive literals)
# this is faster by 50% relative improvement in speed
# ref: http://www.cril.univ-artois.fr/~coste/Articles/coste-etal-sat05.pdf
def jersolow_wang_2_sided_method(cnf):
	literal_weight = defaultdict(int)
	for clause in cnf:
		for literal in clause:
			literal_weight[abs(literal)] += 2 ** -len(clause)
	return max(literal_weight, key=literal_weight.get)

# Boolean Constrain Propagation (see slide 18)
# we set unit to true and so we need to update the cnf by the following rules:
# - Clauses that contain unit are removed (due to "or")
# - Update clauses by removing -unit from them if it exist (due to "or")
def bcp(cnf, unit):
	new_cnf = []
	for clause in cnf:
		if unit in clause:
			continue
		if -unit in clause:
			new_clause = [literal for literal in clause if literal != -unit]
			# base case: conjunct containing an empty disjunct so False
			# but we should continue later because there might be another path
			if not new_clause:
				return -1
			new_cnf.append(new_clause)
		else:
			new_cnf.append(clause)
	return new_cnf

# This implements the while loop of the BCP function (see slide 18)
def assign_unit(cnf):
	I = [] # contains the bool assignments for each variable
	unit_clauses = [clause for clause in cnf if len(clause) == 1]
	while unit_clauses:
		unit = unit_clauses[0][0]
		cnf = bcp(cnf, unit) # assign true to unit
		I += [unit]
		if cnf == -1:
			return -1, []
		# base case: empty conjunct so it is SAT
		if not cnf:
			return cnf, I
		unit_clauses = [clause for clause in cnf if len(clause) == 1] # update
	return cnf, I

# DPLL algorithm is here
def backtrack(cnf, I):
	cnf, unit_I = assign_unit(cnf)
	I = I + unit_I
	if cnf == -1:
		return []
	if not cnf:
		return I
	selected_literal = jersolow_wang_2_sided_method(cnf)
	res = backtrack(bcp(cnf, selected_literal), I + [selected_literal])
	# if no solution when assigning to True, try to assign to False
	if not res:
		res = backtrack(bcp(cnf, -selected_literal), I + [-selected_literal])
	return res

def run_benchmarks():
	print('Running on benchmarks...')
	start_time = time.time()
	for filename in os.listdir("benchmarks"):
		clauses = parse_dimacs(os.path.join("benchmarks", filename))
		assignment = backtrack(clauses, [])
		if assignment:
			print('SAT')
		else:
			print('UNSAT')
	end_time = time.time()
	print('Execution time: %.2f' % (end_time - start_time))

if __name__ == '__main__':
	clauses = parse_dimacs(sys.argv[1])
	assignment = backtrack(clauses, [])
	if assignment:
		print('SAT')
		assignment.sort(key=lambda x: abs(x))
		print(assignment)
	else:
		print('UNSAT')
