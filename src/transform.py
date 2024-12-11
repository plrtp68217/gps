def transform_data(packet_times,
                   lens,
                   accepptances,
                   endtimes,
                   ):
    table_rows = []
    for table_thread in packet_times:
        for table_row in range(len(packet_times[table_thread])):
            second_row = []
            second_row.append(table_thread)  # номер потока
            second_row.append(lens[table_thread][table_row])  # вес пакета
            second_row.append(packet_times[table_thread][table_row])  # время прихода
            second_row.append(accepptances[table_thread][table_row])  # время принятия
            second_row.append(endtimes[table_thread][table_row])  # время обработки
            table_rows.append(second_row)
    return table_rows
