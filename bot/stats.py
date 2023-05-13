import matplotlib.pyplot as plt
import numpy as np


def generate_stats_by_month(month, history):
    months = {1: "январь", 2: "февраль", 3: "март", 4: "апрель", 5: "май", 6: "июнь", 7: "июль", 8: "август",
              9: "сентябрь", 10: "октябрь", 11: "ноябрь", 12: "декабрь"}
    dates = []
    result = []
    cur_sum = 0

    j = 0
    history = list(map(lambda day: day.split(), history))
    for i in range(31):
        if int(history[j][1][:2]) == i:
            operation = history[j][0]
            amount = int(history[j][2])

            if operation == 'Income':
                cur_sum += amount
            elif operation == 'Expense':
                cur_sum -= amount
            j += 1

        result.append(cur_sum)
        dates.append(i)

    y_pos = np.arange(31)
    plt.figure(figsize=(10, 5))
    plt.bar(y_pos, result, align='center', alpha=1, width=1)
    plt.xticks(y_pos, dates)
    plt.ylabel('Баланс')
    plt.title(f'График за {months[month]} месяц 2023')
    plt.savefig(f'график.png')
