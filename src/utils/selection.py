import math
import random


def roulette_selection(population_with_values):
    population_without_zeros = [individual for individual in population_with_values if individual[1] > 0]

    total_values = 0
    for parent in population_without_zeros:
        total_values += parent[1]

    parent_probabilities = []
    cumulative = 0
    for i in range (0, len(population_without_zeros)):
        cumulative += population_without_zeros[i][1] / total_values
        parent_probabilities.append([i, cumulative])

    parent_one_prob = random.random()
    parent_two_prob = random.random()

    parent_one_id = parent_finder(parent_one_prob, parent_probabilities)
    parent_two_id = parent_finder(parent_two_prob, parent_probabilities)

    return population_without_zeros[parent_one_id][0], population_without_zeros[parent_two_id][0]

def parent_finder(p, probability_list):
    for i in range (0, len(probability_list)):
        if i == 0:
            if p <= probability_list[i][1]:
                return probability_list[i][0]
        else:
            if probability_list[i-1][1] < p <= probability_list[i][1]:
                return probability_list[i][0]
    else:
        ModuleNotFoundError("Could not find parent")
        return None

def tournament_selection(population_with_values):
    population_size = len(population_with_values)
    max_size = max(2, int(math.sqrt(population_size)))
    tournament_size = random.randint(2, int(math.sqrt(population_size)))
    winners = []
    population_without_zeros = [individual for individual in population_with_values if individual[1] > 0]

    for _ in range(tournament_size):
        candidates = random.sample(population_without_zeros, tournament_size)
        winner = max(candidates, key=lambda x: x[1])
        winners.append(winner)
    return winners[0], winners[1]


def ranking_selection(population_with_values):
    population_without_zeros = [individual for individual in population_with_values if individual[1] > 0]
    population_without_zeros.sort(key=lambda x: x[1], reverse=True)
    size = len(population_without_zeros)
    ranks = list(range(1, size+1))
    total_rank = sum(ranks)
    probabilities = [(size - rank + 1) / total_rank for rank in ranks]

    cumulative = []
    total = 0

    for p in probabilities:
        total += p
        cumulative.append(total)

    parent_one_prob = random.random()
    parent_two_prob = random.random()

    parent_one_id = parent_finder(parent_one_prob, list(enumerate(cumulative)))
    parent_two_id = parent_finder(parent_two_prob, list(enumerate(cumulative)))

    return population_without_zeros[parent_one_id][0], population_without_zeros[parent_two_id][0]

    print(cumulative)

