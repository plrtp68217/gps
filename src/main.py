from generators import generate_exp_time, generate_exp_len
from fractions import Fraction
import matplotlib.pyplot as plt
from tabulate import tabulate

number_of_threads = 2 # число потоков

thread_priorities = [1, 2] # приоритеты каждого потока

active_threads = {} # активные потоки (обрабатывающие пакеты) (0 - не активен, 1 - активен)

completed_threads = {} # потоки, обработавшие все пакеты (true - обработал все, false - не обработал)

len_thread = {} # суммарный вес обработанных пакетов на каждой обработке

packets_time = {} # время прихода пакетов для каждого потока

packets_acceptance = {} # время принятия пакета на обработку

packets_endtime = {} # время обработки пакетов для каждого потока

packets_handling = {} # процесс обработки пакетов

packets_len = {} # длина поступивших пакетов для каждого потока

time_tracker = {} # какие прибывшие пакеты были переведены в обработку

processing = True # индикатор, отображающий работу планировщика (при обработке всех пакетов перевести в false)

cycle_counter = 0 # счетчик циклов работы панировщика (каждый пройденный цикл - единица времени работы панировщика)

packets_time = {
    1: [1, 2, 3, 11],
    2: [0, 5, 9]
}

packets_len = {
    1: [1, 1, 2, 2],
    2: [3, 2, 2]
}


for thread in range(number_of_threads):
    # packets_time[thread + 1] = generate_exp_time()
    packets_acceptance[thread + 1] = []
    packets_endtime[thread + 1] = []
    # packets_len[thread + 1] = generate_exp_len(packets_time[thread + 1])
    time_tracker[thread + 1] = [0]
    packets_handling[thread + 1] = []
    len_thread[thread + 1] = [0]
    active_threads[thread + 1] = 0
    completed_threads[thread + 1] = False


while processing:
    # проверка неактивных потоков
    for thread in packets_time:
        if active_threads[thread] == 0 and completed_threads[thread] == False: # если поток неактивен и еще не обработал все пакеты
            packet_index = time_tracker[thread][-1]
            if cycle_counter >= packets_time[thread][time_tracker[thread][-1]]:
                packets_acceptance[thread].append(cycle_counter)
                packets_handling[thread].append(packet_index) # индекс рассматриваемого пакета
                packets_handling[thread].append(packets_len[thread][packet_index]) # длина рассматриваемого пакета
                packets_handling[thread].append(0) # сколько информационных единиц было обработано
                active_threads[thread] = 1 # перевод потока в активное состояние

    # рассчет скорости обработки относительно активных потоков
    summary = 0 # знаменатель скорости обработки (в числителе будет приоритет рассматриваемого потока)

    for active_thread in range(len(active_threads)): 
        if active_threads[active_thread + 1] == 1:
            summary += thread_priorities[active_thread]

    # обработка пакетов активных потоков
    for processing_thread in range(len(active_threads)):
        if active_threads[processing_thread + 1] == 1:
            packets_handling[processing_thread + 1][2] += Fraction(thread_priorities[processing_thread], summary) # обрабатываем пакет на величину текущей загрузки (приоритет потока / summary)
            if packets_handling[processing_thread + 1][2] >= packets_handling[processing_thread + 1][1]: #если пакет обработан
                active_threads[processing_thread + 1] = 0 # переводим поток в состояние неактивного
                packets_endtime[processing_thread + 1].append(cycle_counter + 1) # записываем время, когда пакет был обработан
                len_thread[processing_thread + 1].append(len_thread[processing_thread + 1][-1] + packets_handling[processing_thread + 1][1])
                packets_handling[processing_thread + 1].clear()
                if len(time_tracker[processing_thread + 1]) < len(packets_time[processing_thread + 1]):
                    time_tracker[processing_thread + 1].append(time_tracker[processing_thread + 1][-1] + 1)
                elif len(time_tracker[processing_thread + 1]) == len(packets_time[processing_thread + 1]):
                    completed_threads[processing_thread + 1] = True
    
    # проверка на факт обработки всех пакетов всеми потоками
    end_processing = True

    for second_thread in packets_time:
        end_processing = end_processing and completed_threads[second_thread]

    if end_processing: # если все пакеты обработаны
        processing = False # завершить работу планировщика

    # переход на следующую временную единицу
    cycle_counter += 1

# print('время прихода пакета', packets_time)
# print('время принятия пакета в обработку' ,packets_acceptance)
# print('время обработки пакета', packets_endtime)
# print('веса', len_thread)


#преобразуем полученные данные для вывода в табличном виде

table_result = []
table_headers = ['Номер потока', 'Вес пакета', 't прихода', 't принятия', 't обработки']

for table_thread in packets_time:
    for table_row in range(len(packets_time[table_thread])):
        second_row = []
        second_row.append(table_thread) # номер потока
        second_row.append(packets_len[table_thread][table_row]) # вес пакета
        second_row.append(packets_time[table_thread][table_row]) # время прихода
        second_row.append(packets_acceptance[table_thread][table_row]) # время принятия
        second_row.append(packets_endtime[table_thread][table_row]) # время обработки
        table_result.append(second_row)

print(tabulate(table_result, headers=table_headers, tablefmt='grid'))


# строим графики
for plot_thread in packets_time:
    for sub_plots in range(len(packets_time[plot_thread])):
        plt.subplot(number_of_threads, 1, plot_thread)
        plt.plot([packets_acceptance[plot_thread][sub_plots], packets_endtime[plot_thread][sub_plots]], # x
                 [len_thread[plot_thread][sub_plots], len_thread[plot_thread][sub_plots + 1]], label=f'{len_thread[plot_thread][sub_plots + 1]}') # y
        plt.title(f'Поток {plot_thread}', loc='left', fontdict={'fontsize': 8,
                                                                'fontweight': 'bold',})
    plt.ylabel("Время, ед.")

plt.xlabel("Данные, бит") # выводим подпись для оси x только для последнего графика

plt.show()












