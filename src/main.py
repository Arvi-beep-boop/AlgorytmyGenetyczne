import argparse
from pathlib import Path

from src.population import get_population
from utils import *

VALUE_IDX = 0
WEIGHT_IDX = 1

PARSER = argparse.ArgumentParser(
    prog='Backpack Problem',
    description='Backpack Problem for university assignment',
)

PARSER.add_argument('-ic', '--iteration_count', type=int, default=10, help='Number of iterations')
PARSER.add_argument('-p', '--population_size', type=int, default=50, help='Population size')
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
    print(args.iteration_count)
    read_data(filepath, backpack)
    print(backpack)
    print(filepath)
    population = get_population(args.population_size, backpack[0][0])
    for elem in population:
        print(elem)

    one_point_crossover(population[0], population[1])
    two_point_crossover(population[0], population[1])
    first = population[0]
    sample = mutate(.5, population[0])

    print(sample)

if __name__ == '__main__':
    main()