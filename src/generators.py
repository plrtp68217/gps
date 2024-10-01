import random

def generate_exp_time() -> list:
    ''' Формирует случайное время прихода пакетов'''
    rate = 0.5
    exp_time = set([round(10 * random.expovariate(rate)) for _ in range(10)])
    return sorted(exp_time)

def generate_exp_len(packets: list) -> list:
    ''' Формирует случайные длины для пакетов'''
    exp_len = [round(10 * random.random()) + 1 for _ in packets]
    return exp_len
