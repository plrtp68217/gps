import tkinter as tk
from tkinter import ttk

def showTable(headers: list, data: list):
    '''
    Вывод окна с таблицей.
    headers - ['столбец 1, столбец 2, ...'].
    data - [[1, 10, ...], [12, 20, ...]].
    '''
    # Создаём окно
    root = tk.Tk()
    root.title("Результаты")

    # Создаём Treeview (таблицу)
    tree = ttk.Treeview(root, columns=headers, show="headings")

    # Добавляем заголовки
    for col in headers:
        tree.heading(col, text=col)

    # Добавляем данные
    for row in data:
        tree.insert("", tk.END, values=row)

    # Добавляем вертикальную прокрутку
    scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    # Размещаем элементы
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Запускаем приложение
    return root