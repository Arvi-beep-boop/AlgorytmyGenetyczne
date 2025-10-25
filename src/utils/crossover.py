import random

def one_point_crossover(parent1, parent2):
    max_point = len(parent1) - 1
    min_point = 1
    crossover_point = random.randint(min_point, max_point)
    new_parent1 = parent1[:crossover_point] + parent2[crossover_point:]
    new_parent2 = parent2[:crossover_point] + parent1[crossover_point:]
    return new_parent1, new_parent2

def two_point_crossover(parent1, parent2):
    max_point = len(parent1) - 1
    min_point = 1
    crossover_point_1 = random.randint(min_point, max_point)
    crossover_point_2 = random.randint(min_point, max_point)
    while True:
        if crossover_point_1 != crossover_point_2: break
        crossover_point_2 = random.randint(min_point, max_point)
    min_val, max_val = min(crossover_point_1, crossover_point_2), max(crossover_point_1, crossover_point_2)
    new_parent1 = parent1[:min_val] + parent2[min_val:max_val] + parent1[max_val:]
    new_parent2 = parent2[:min_val] + parent1[min_val:max_val] + parent2[max_val:]
    return new_parent1, new_parent2

