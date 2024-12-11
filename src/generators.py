import random

def generate_exp_time(max_packets: int) -> list:
    '''Формирует случайное время прихода пакетов'''
    number_of_packets = int(max_packets * random.random()) # максимальное число пакетов
    rate = 0.5
    exp_time = [round(10 * random.expovariate(rate)) for _ in range(number_of_packets)]
    return sorted(exp_time)

def generate_exp_len(packets: list) -> list:
    '''Формирует случайные длины для пакетов'''
    exp_len = [round(10 * random.random()) + 1 for _ in packets]
    return exp_len