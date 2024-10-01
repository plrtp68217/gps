from generators import generate_exp_time, generate_exp_len

number_of_threads = 3 # число потоков

thread_priorities = [1, 2, 3] # приоритеты каждого потока

active_threads = {} # активные потоки (обрабатывающие пакеты) (0 - не активен, 1 - активен)

packets_time = {} # время прихода пакетов для каждого потока

packets_endtime = {} # время обработки пакетов для каждого потока

time_tracker = {} # какие прибывшие пакеты были переведены в обработку

packets_handling = {} # процесс обработки пакетов 

packets_len = {} # длина поступивших пакетов для каждого потока

processing = True # индикатор, отображающий работу планировщика (при обработке всех пакетов перевести в false)

cycle_counter = 0 # счетчик циклов работы панировщика (каждый пройденный цикл - единица времени работы панировщика)

for thread in packets_time:
    packets_time[thread] = generate_exp_time()
    packets_len[thread] = generate_exp_len(packets_time[thread + 1])
    time_tracker[thread] = [0]
    packets_handling[thread] = []
    active_threads[thread] = 0


while processing:
    # проверка неактивных потоков
    for thread in packets_time:
        if active_threads[thread] == 0:
            packet_index = time_tracker[thread][-1]
            if cycle_counter >= packets_time[thread][time_tracker[thread][-1]]:
                packets_handling[thread].append(packet_index) # индекс рассматриваемого пакета
                packets_handling[thread].append(packets_len[thread][packet_index]) # длина рассматриваемого пакета
                packets_handling[thread].append(0) # сколько информационных единиц было обработано
                active_threads[thread] = 1 # перевод потока в активное состояние

    # рассчет скорости обработки относительно активных потоков
    summary = 0 # знаменатель скорости обработки (в числителе будет приоритет рассматриваемого потока)
    for active_thread in range(len(active_threads)): 
        if active_threads[active_thread] == 1:
            summary += thread_priorities[active_thread]

    # обработка пакетов активных потоков
    for processing_thread in range(len(active_threads)):
        if active_threads[processing_thread] == 1:
            packets_handling[processing_thread + 1][2] += thread_priorities[processing_thread] / summary # обрабатываем пакет на величину загрузки (приоритет потока / summary)
        if packets_handling[processing_thread + 1][2] >= packets_handling[processing_thread + 1][1]: #если пакет обработан
            packets_handling[processing_thread + 1].clear()
            active_threads[processing_thread] = 0 # переводим поток в состояние неактивного
            packets_endtime[processing_thread + 1].append(cycle_counter)
            if len(time_tracker[processing_thread + 1]) < len(packets_time[processing_thread + 1]):
                time_tracker[processing_thread + 1].append(time_tracker[processing_thread + 1][-1] + 1)

















