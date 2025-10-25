import random

def get_population(population_size, problem_size):
    population = []
    for i in range(population_size):
        creature = []
        for j in range(problem_size):
            creature.append(random.randint(0,1))
        population.append(creature)
    return population