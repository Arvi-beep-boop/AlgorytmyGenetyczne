
def is_adaptive(creature, backpack):
    sum_weights = 0
    max_sum_weights = backpack[0][1]
    for i in range(0, len(creature)):
        if creature[i] > 0:
            sum_weights += backpack[i+1][1]
    return  sum_weights <= max_sum_weights

def get_adaptive(population, backpack):
    new_population = []
    for creature in population:
        is_ok = is_adaptive(creature, backpack)
        if is_ok:
            new_population.append(creature)
    return new_population