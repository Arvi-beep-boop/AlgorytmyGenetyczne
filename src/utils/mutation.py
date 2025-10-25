import random

def mutate(probability, node):
    new_node = node.copy()
    for i in range(0, len(node)):
        if random.random() <= probability:
            new_node[i] = 1 if new_node[i] == 0 else 0
    return new_node

