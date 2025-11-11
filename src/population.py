import random

def get_population(population_size, problem_size, backpack):
    population = []
    max_weight = backpack[0][1]
    for i in range(population_size):
        creature = []
        creature_weight = 0
        for j in range(problem_size):
            if creature_weight < max_weight:
                value = random.randint(0,1)
                if value > 0:
                    new_weight = creature_weight + backpack[j+1][1]
                    if new_weight > max_weight:
                        creature.append(0)
                    else:
                        creature_weight += backpack[j+1][1]
                        creature.append(value)
                        continue
                else:
                    creature.append(value)
            else:
                creature.append(0)
        population.append(creature)
    return population