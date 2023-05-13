import datetime
import matplotlib.pyplot as plt
import numpy as np


def generate_stats_by_month(month, history):
    dates = []
    result = []
    cur_sum = 0

    for entry in history:
        parts = entry.split(' ')
        operation = parts[0]
        date = datetime.datetime.strptime(parts[1], '%d.%m.%Y')
        amount = int(parts[2])

        if operation == 'Income':
            cur_sum += amount
        elif operation == 'Expense':
            cur_sum -= amount

        result.append(cur_sum)
        dates.append(date)

    y_pos = np.arange(len(dates))
    plt.bar(y_pos, result, align='center', alpha=0.5)
    plt.xticks(y_pos, dates)
    plt.ylabel('Сумма')
    plt.title(f'График за {month} 2023')
    plt.savefig(f'график.png')
