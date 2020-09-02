#!/usr/bin/env bash

"""
Multiple Knapsack problem example
"""


from __future__ import print_function
from ortools.linear_solver import pywraplp
from tqdm import tqdm

import random



def create_data_model():
    """Create the data for the example."""
    data = {}
    num = 50000
    peaks = [random.randint(20, 100) for i in range(num)]
    data['weights'] = [1] * num
    data['values'] = [x + 2 for x in peaks]
    data['items'] = list(range(num))
    data['num_items'] = num
    data['bins'] = list(range(num))
    data['bin_capacities'] = peaks
    return data




def main():
    print('Generate Data')
    data = create_data_model()
    print('DONE')

    # Create the mip solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('multiple_knapsack_mip', 'CBC')

    # Variables
    # x[i, j] = 1 if item i is packed in bin j.
    print('Add variables to bin')
    x = {}
    for i in tqdm(data['items']):
        for j in data['bins']:
            x[(i, j)] = solver.IntVar(0, 1, 'x_%i_%i' % (i, j))

    # Constraints
    # Each item can be in at most one bin.
    print('Add constraints placed once')
    for i in tqdm(data['items']):
        solver.Add(sum(x[i, j] for j in data['bins']) <= 1)
    # The amount packed in each bin cannot exceed its capacity.
    print('Add constraints max capacity')
    for j in tqdm(data['bins']):
        solver.Add(
            sum(x[(i, j)] * data['weights'][i]
                for i in data['items']) <= data['bin_capacities'][j])

    # Objective
    print('Start solver')
    objective = solver.Objective()
    print('Finished solving')

    for i in data['items']:
        for j in data['bins']:
            objective.SetCoefficient(x[(i, j)], data['values'][i])
    objective.SetMaximization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Total packed value:', objective.Value())
        total_weight = 0
        for j in data['bins']:
            bin_weight = 0
            bin_value = 0
            print('Bin ', j, '\n')
            for i in data['items']:
                if x[i, j].solution_value() > 0:
                    print('Item', i, '- weight:', data['weights'][i], ' value:',
                          data['values'][i])
                    bin_weight += data['weights'][i]
                    bin_value += data['values'][i]
            print('Packed bin weight:', bin_weight)
            print('Packed bin value:', bin_value)
            print()
            total_weight += bin_weight
        print('Total packed weight:', total_weight)
    else:
        print('The problem does not have an optimal solution.')


if __name__ == '__main__':
    main()