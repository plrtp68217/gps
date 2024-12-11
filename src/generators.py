import random

def generate_exp_time(max_packets: int) -> list:
    '''
    Формирует случайное время прихода пакетов
    max-packets - максимальное число прибывших пакетов
    '''
    number_of_packets = int(max_packets * random.random()) + 1 # максимальное число пакетов
    rate = 0.5
    exp_time = [int(10 * random.expovariate(rate)) for _ in range(number_of_packets)]
    return sorted(exp_time)

def generate_exp_len(packets: list) -> list:
    '''Формирует случайные вещественные длины для пакетов в диапазоне [0, 30]'''
    exp_len = [round(30 * random.random(), 2) for _ in packets]
    return exp_len