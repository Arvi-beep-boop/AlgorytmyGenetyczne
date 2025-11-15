import math
import random

def get_population(population_size, problem_size, backpack):
    population = []
    max_weight = backpack[0][1]
    for i in range(population_size):
        creature = [0 for _ in range(problem_size)]
        creature_weight = 0
        while creature_weight < max_weight:
            index = random.randint(0, problem_size-1)
            new_weight = creature_weight + backpack[index+1][1]
            if new_weight < max_weight:
                creature[index] = 1
                creature_weight += backpack[index+1][1]
            else:
                break
            if random.random() <= (1/math.sqrt(problem_size)):
                break
        population.append(creature)
    return population