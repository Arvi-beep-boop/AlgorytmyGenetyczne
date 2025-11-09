import argparse
from pathlib import Path

from src.population import get_population
from utils import *

## METHODS

crossover_methods = {
    "one_point": one_point_crossover,
    "two_point": two_point_crossover,
}

selection_methods = {
    "tournament": tournament_selection,
    "roulette": roulette_selection,
    "ranking": ranking_selection,
}

VALUE_IDX = 0
WEIGHT_IDX = 1

PARSER = argparse.ArgumentParser(
    prog='Backpack Problem',
    description='Backpack Problem for university assignment',
)

PARSER.add_argument('-ic', '--iteration_count', type=int, default=10, help='Number of iterations')
PARSER.add_argument('-p', '--population_size', type=int, default=50, help='Population size')
PARSER.add_argument('-m', '--mutation_rate', type=float, default=0.08, help='Mutation rate, 0.0-0.1 recommended')
PARSER.add_argument('-cr', '--crossover_rate', type=float, default=0.7, help='Crossover rate, 0.5-1.0 recommended')
PARSER.add_argument("--crossover", choices=crossover_methods.keys(), default="one_point", help="Crossover method: one_point or two_point")
PARSER.add_argument("--selection", choices=selection_methods.keys(), default="roulette", help="Selection method: tournament, roulette or ranking")
PARSER.add_argument('-f', '--file', type=Path, help='File path')
args = PARSER.parse_args()
filepath = args.file.resolve()

ITERATION_COUNT = args.iteration_count
backpack = []


def read_data(filepath, backpack):
    # EXPECTED FILE STRUCTURE:
    # Wielkosc_problemu pojemnosc
    # wartosc_przedmiotu_1 waga_przedmiotu_1
    # ....
    # wartosc_przedmiotu_n waga_przedmiotu_n

    #wagi przedmiotu nie mogą przekraczać pojemności, wartość chcemy jak największą
    with open(filepath, 'r') as file:
        while True:
            line = file.readline().strip()
            if not line:
                break
            data = list(map(int, line.split()))
            backpack.append(data)

# read_data('../dane AG/low-dimensional/f1_l-d_kp_10_269', backpack)




def main():
    # print(backpack)

    """
    1. process args etc
    2. get the start population
    3. start iteration
    4. check if the sum of weight does not exceed
    5. select the creatures
    6. genetic operators
    7. new population created
    done

    in the meantime save the data to make a chart
    """
    # chose the methods from args
    crossover_function = crossover_methods[args.crossover]
    selection_function = selection_methods[args.selection]

    read_data(filepath, backpack)

    # maybe I'll use this for charts/graphs idk
    population_history = []
    best_in_given_iteration = []
    population = get_population(args.population_size, backpack[0][0])

    for _ in range(ITERATION_COUNT):
        adaptive_with_values = get_adaptive_with_values(population, backpack)
        # save the best sample from adaptive with values before mutating etc
        population_history.append(adaptive_with_values)
        best = max(adaptive_with_values, key=lambda x: x[1])
        best_in_given_iteration.append(best)

        new_population = []
        for i in range(0, int(args.population_size/2)):
            # select 2 parents
            parent_one, parent_two = selection_function(adaptive_with_values)
            # crossover
            child_one, child_two = crossover_function(parent_one, parent_two, args.crossover_rate)
            # mutation
            child_one = mutate(args.mutation_rate, child_one)
            child_two = mutate(args.mutation_rate, child_two)
            # saving to new population
            new_population.append(child_one)
            new_population.append(child_two)
        # replacing population
        population = new_population


if __name__ == '__main__':
    main()