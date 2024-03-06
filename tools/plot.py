import matplotlib.dates as mdates
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon, Rectangle


class PlotService:
    low_border = 4
    high_border = 20.2
    warning = 10
    critical = 19

    @classmethod
    def current_level(cls, level: float):
        def draw_tank(axs: Axes):
            coordinates = np.array([
                (1, cls.low_border),
                (1, cls.high_border),
                (2, cls.high_border),
                (2, 21),
                (5, 21),
                (5, cls.high_border),
                (11, cls.high_border),
                (11, cls.low_border)])
            tank = Polygon(coordinates, fill=False, closed=True)
            axs.add_patch(tank)

        def draw_pump_level(axs: Axes):
            line = Line2D([9, 11], [cls.warning, cls.warning], color='yellow')
            axs.add_line(line)
            plt.text(11.5, cls.warning, 'критический \n уровень 1')

        def draw_critical_level(axs: Axes):
            line = Line2D([9, 11], [cls.critical, cls.critical], color='red')
            axs.add_line(line)
            plt.text(11.5, cls.critical, 'критический \n уровень 2')

        def draw_liquid(axs: Axes, lvl: float = level):
            start_point = (1.1, cls.low_border+0.1)
            width = 9.8
            height = lvl - cls.low_border
            liquid = Rectangle(start_point, width, height, color='skyblue')
            axs.add_patch(liquid)

        plt.clf()
        axes = plt.gca()
        axes.set_aspect('equal')
        draw_tank(axes)
        draw_liquid(axes)
        draw_critical_level(axes)
        draw_pump_level(axes)
        axes.set_xlim(0, 17)
        axes.set_ylim(3, 22)
        axes.set_xticks([])
        axes.set_yticks([])
        plt.title('Текущий уровень')
        plt.savefig('media/curr_level.png')

    @classmethod
    def archive_levels(cls, data: list):
        x_vals = [i['timestamp'] for i in data]
        day = x_vals[0].date()
        print(day, type(day))
        y_vals = [i['level'] for i in data]
        date_format = mdates.DateFormatter('%H:%M')
        plt.clf()
        plt.gca().xaxis.set_major_formatter(date_format)
        plt.plot(x_vals, y_vals)
        plt.plot(x_vals, [cls.warning] * len(x_vals), color='yellow', label='крит.ур.1')
        plt.plot(x_vals, [cls.critical] * len(x_vals), color='red', label='крит.ур.2')
        plt.fill_between(x_vals, y_vals, color='skyblue')
        plt.title(f"Изменение уровня за {day}")
        plt.xlabel("Время")
        plt.ylabel("Уровень")
        plt.yticks([])
        plt.legend()
        plt.savefig('media/l_history.png')
