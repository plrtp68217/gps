from generators import generate_exp_values

number_of_threads = 3 # число потоков

packets_time = {} # время прихода пакетов для каждого потока

packets_len = {} # длина поступивших пакетов для каждого потока

for thread in range(number_of_threads):
    packets_time[thread + 1] = generate_exp_values()


