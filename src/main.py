from generators import generate_exp_time, generate_exp_len

number_of_threads = 3 # число потоков

thread_priorities = [1, 2, 3] # приоритеты каждого потока

packets_time = {} # время прихода пакетов для каждого потока

packets_endtime = {} # время обработки пакетов для каждого потока

packets_len = {} # длина поступивших пакетов для каждого потока

processing = True # индикатор, отображающий работу планировщика (при обработке всех пакетов перевести в false)

cycle_counter = 0 # счетчик циклов работы панировщика (каждый пройденный цикл - единица времени работы панировщика)

for thread in range(number_of_threads):
    packets_time[thread + 1] = generate_exp_time()
    packets_len[thread + 1] = generate_exp_len(packets_time[thread + 1])


# while processing:
#     for 















