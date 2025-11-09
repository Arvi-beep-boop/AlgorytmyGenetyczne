import random


def roulette_selection(population_with_values):
    # for each parent index (0, 1, 2 etc) I'll make an array of the probabilities of it being picked.
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

    parent_one_id = roulette_parent_finder(parent_one_prob, parent_probabilities)
    parent_two_id = roulette_parent_finder(parent_two_prob, parent_probabilities)

    return parent_one_id, parent_two_id

def roulette_parent_finder(p, probability_list):
    for i in range (0, len(probability_list)):
        if i == 0:
            if p <= probability_list[i][1]:
                return probability_list[i][0]
        else:
            if probability_list[i-1][1] < p <= probability_list[i][1]:
                return probability_list[i][0]
    else:
        return -1


def tournament_selection():
    print("tournament")

def ranking_selection():
    print("ranking")