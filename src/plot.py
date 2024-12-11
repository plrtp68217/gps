import matplotlib.pyplot as plt

def show_plot(packet_times,
              number_threads,
              acceptances,
              endtimes,
              len_threads,
              ):
    for plot_thread in packet_times:
        for sub_plots in range(len(packet_times[plot_thread])):
            plt.subplot(number_threads, 1, plot_thread)
            plt.plot([acceptances[plot_thread][sub_plots], endtimes[plot_thread][sub_plots]],  # x
                     [len_threads[plot_thread][sub_plots], len_threads[plot_thread][sub_plots + 1]],
                     label=f'{len_threads[plot_thread][sub_plots + 1]}')  # y
            plt.title(f'Поток {plot_thread}', loc='left', fontdict={'fontsize': 8,
                                                                    'fontweight': 'bold', })
        plt.ylabel("Данные, бит")

    plt.xlabel("Время, ед.")  # выводим подпись для оси x только для последнего графика

    plt.show()