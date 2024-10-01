import random

def generate_exp_values():
    rate = 0.5
    exp_values = set([round(10 * random.expovariate(rate)) for i in range(10)])
    return sorted(exp_values)
