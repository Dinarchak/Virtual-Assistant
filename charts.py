from settings import config
from matplotlib.ticker import MultipleLocator
from repository import Repository
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np

class Chart:
    @staticmethod
    def week_stat(engine, start_time, end_time):
        repo = Repository(engine)
        query = repo.daily_time_query(start_time, end_time)

        species = (
            'Понедельник',
            'Вторник',
            'Среда',
            'Четверг',
            'Пятница',
            'Суббота',
            'Воскресенье'
        )

        weight_counts = {}
        for i in query:
            if i.name not in weight_counts:
                weight_counts[i.name] = np.zeros(7)
            weight_counts[i.name][i.day - start_time.day] = i.delta // 60
        
        bottom = np.zeros(7)
        fig, axes = plt.subplots(2, 1)
        ax1, ax2 = axes

        for label, weight in weight_counts.items():
            ax1.bar(species, weight, label=label, bottom=bottom)
            bottom += weight

        for label, weight in weight_counts.items():
            ax2.plot(species, weight, label=label)

        ax1.legend(loc='upper right')
        ax1.yaxis.set_major_locator(MultipleLocator(base=30))
        ax1.yaxis.set_minor_locator(MultipleLocator(base=15))
        ax1.yaxis.set_major_formatter(lambda x, _: (start_time + timedelta(minutes=x)).strftime('%H:%M'))

        ax2.legend(loc='upper right')
        ax2.yaxis.set_major_locator(MultipleLocator(base=15))
        ax2.yaxis.set_minor_locator(MultipleLocator(base=5))
        ax2.yaxis.set_major_formatter(lambda x, _: (start_time + timedelta(minutes=x)).strftime('%H:%M'))

        fig.canvas.manager.set_window_title("Недельная статистика")
        plt.show()

    @staticmethod
    def daily_stat(engine, start_time, end_time):
        repo = Repository(engine)
        q1 = repo.bar_query(start_time, end_time)
        q2 = repo.scale_query(start_time, end_time)

        processes = []
        data = []
        ranges = {}

        for i in q1:
            processes.append(i.name)
            data.append(i.delta // 60)

        for i in q2:
            if i.name not in ranges:
                ranges[i.name] = [((i.start - start_time).total_seconds() // 60, (i.end - i.start).total_seconds() // 60)]
            else:
                ranges[i.name].append(((i.start - start_time).total_seconds() // 60, (i.end - i.start).total_seconds() // 60))

        fig, axes = plt.subplots(2, 1)

        axes[0].yaxis.set_major_locator(MultipleLocator(base=30))
        axes[0].yaxis.set_minor_locator(MultipleLocator(base=5))

        axes[0].yaxis.set_major_formatter(lambda x, pos: (start_time + timedelta(minutes=x)).strftime('%H:%M'))
        axes[0].bar(processes, data, align='center')


        for i, k in enumerate(ranges.keys()):
            axes[1].broken_barh(ranges[k], (i + .8, .4))

        axes[1].set_yticks([1 + i for i in range(len(ranges.keys()))], list(ranges.keys()))

        axes[1].set_xlim(0, (end_time - start_time).total_seconds() // 60)
        axes[1].xaxis.set_major_locator(MultipleLocator(base=60))
        axes[1].xaxis.set_minor_locator(MultipleLocator(base=15))
        axes[1].xaxis.set_major_formatter(lambda x, pos: (start_time + timedelta(minutes=x)).strftime('%H:%M'))
        plt.xticks(rotation=45)

        fig.canvas.manager.set_window_title("Cтатистика за " + datetime.strftime(start_time, config['datetime_str_format']))
        plt.show()

