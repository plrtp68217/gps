from fractions import Fraction
import threading

from generators import generate_exp_time, generate_exp_len
from table import show_table
from plot import show_plot
from transform import transform_data


number_of_threads = 0 # число потоков

thread_priorities = [] # приоритеты каждого потока

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

# ввод исходных данных
input_parameters = eval(input('\nВвод входных параметров: [[n1, n2], [w1, w2].\n'
                              'Где n1 - номер 1 потока,w1 - приоритет 1 потока.\n'
                              'Пример: [[1, 2], [2, 3]]\n: '))

number_of_threads = len(input_parameters)
thread_priorities = input_parameters[1]

#инициализация начальных значений
for thread in range(number_of_threads):
    packets_time[thread + 1] = generate_exp_time(20)
    packets_acceptance[thread + 1] = []
    packets_endtime[thread + 1] = []
    packets_len[thread + 1] = generate_exp_len(packets_time[thread + 1])
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

#преобразуем полученные данные для вывода в табличном виде
table_headers = ['Номер потока', 'Вес пакета', 't прихода', 't принятия', 't обработки']
table_rows = transform_data(packets_time, packets_len, packets_acceptance, packets_endtime)


def show_table_thread():
    # выводим результирующие данные в табличном виде
    show_table(table_headers, table_rows)

if __name__ == "__main__":
    #вывод таблицы в дополнительном потоке
    thread = threading.Thread(target=show_table_thread)
    thread.start()

    # вывод графиков в основном потоке
    show_plot(packets_time, number_of_threads, packets_acceptance, packets_endtime, len_thread)














