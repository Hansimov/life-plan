# %%
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
import pandas as pd
import datetime

plt.rcParams["font.sans-serif"] = ["Microsoft Yahei"]
plt.rc("axes", unicode_minus=False)


class DataParser:
    def __init__(self, data_filename="data.csv"):
        self.df = pd.read_csv(data_filename)
        self.action_zh_en_dict = {
            "日期": "date",
            "编程": "code",
            "交易": "trade",
            "健身": "body",
            "读书": "read",
        }
        self.action_en_zh_dict = dict((v, k) for k, v in self.action_zh_en_dict.items())
        self.df.rename(columns=self.action_zh_en_dict, inplace=True)
        self.df["date"] = pd.to_datetime(self.df["date"])


class CalendarPlotter:
    def __init__(self, data_filename="data.csv"):
        self.aspect = 8
        self.action_color_dict = {
            "code": "#00BBDD",  # light blue
            "trade": "#00EE00",  # green
            "body": "#FF00EE",  # pink
            "read": "#FFFF00",  # yellow
        }
        self.weekday_zh_list = ["日", "一", "二", "三", "四", "五", "六"]
        self.data_parser = DataParser(data_filename)
        self.df = self.data_parser.df
        self.fontsize = 8

    def plot(self):
        fig, self.ax = plt.subplots(dpi=200)
        self.ax.set_aspect(self.aspect)
        self.ax.axis("off")

        row0 = self.df.iloc[[0]]
        self.wk_offset = row0["date"][0].isoweekday()
        self.rect_x_len = 1
        self.rect_y_len = self.rect_x_len / self.aspect
        self.rect_y_gap = 2.5
        self.calendar_bottom = self.rect_y_len * (-self.rect_y_gap) * 6
        for ida, row in self.df.iterrows():
            rect_x, rect_y = self.plot_daily_rects(ida, row)
            self.plot_day_month_texts(
                row["date"],
                rect_x,
                rect_y,
                is_last_day=(ida == self.df.shape[0] - 1),
            )
        self.plot_week_texts()
        self.plot_legends()
        self.plot_bars()

        self.ax.plot()
        # plt.show()
        plt.savefig("calendar.png")

    def plot_daily_rects(self, ida, row):
        for idb, (action, color) in enumerate(self.action_color_dict.items()):
            rect_x = self.rect_x_len * (
                (idb % 2) + self.rect_y_gap * ((ida + self.wk_offset) // 7)
            )
            rect_y = self.rect_y_len * (
                (idb // 2) - self.rect_y_gap * ((ida + self.wk_offset) % 7)
            )
            facecolor = color if row[action] == 1 else "white"
            rect = Rectangle(
                (rect_x, rect_y),
                *(self.rect_x_len, self.rect_y_len),
                facecolor=facecolor,
                edgecolor="gray",
            )
            self.ax.add_patch(rect)
        self.calendar_right = rect_x + self.rect_x_len * 2
        return rect_x, rect_y

    def plot_day_month_texts(self, date, rect_x, rect_y, is_last_day=False):
        # Plot day texts
        day_text_x = rect_x + self.rect_x_len / 10
        day_text_y = rect_y + self.rect_y_len / 8
        date_text_str = f"{date.day:01}"
        plt.text(day_text_x, day_text_y, date_text_str, fontsize=self.fontsize / 1.6)

        # Plot month texts
        if date.isoweekday() == 6 or is_last_day:
            month_text_x = rect_x
            # month_text_y = rect_y - self.rect_y_len * 1.5
            month_text_y = self.calendar_bottom - self.rect_y_len * 0.5
            month_text_str = f"{date.month}"
            # month_text_str = date.strftime("%b")
            one_week_delta = datetime.timedelta(days=7)
            if date.month == (date - one_week_delta).month:
                color, fontweight = "black", "normal"
            else:
                color, fontweight = "blue", "bold"
            plt.text(
                month_text_x,
                month_text_y,
                month_text_str,
                va="top",
                ha="center",
                color=color,
                fontsize=self.fontsize,
                fontweight=fontweight,
            )

    def plot_week_texts(self):
        for i in range(7):
            weekday_text_y = self.rect_y_len * (-self.rect_y_gap * i + 1)
            # weekday_text_x = self.rect_x_len * (-1.0)
            weekday_text_x = self.calendar_right
            weekday_text_str = self.weekday_zh_list[i]
            if i not in [0, 6]:
                color, fontweight = "black", "normal"
            else:
                color, fontweight = "blue", "bold"

            plt.text(
                weekday_text_x,
                weekday_text_y,
                weekday_text_str,
                va="center",
                ha="left",
                color=color,
                fontsize=self.fontsize,
                fontweight=fontweight,
            )

    def plot_legends(self):
        handles = []
        for idb, (action, color) in enumerate(self.action_color_dict.items()):
            patch = Patch(color=color, label=self.data_parser.action_en_zh_dict[action])
            handles.append(patch)
        plt.legend(handles=handles, bbox_to_anchor=(0.0, 0.98), fontsize=self.fontsize)

    def plot_bars(self):
        self.bar_width = self.calendar_right / self.df.shape[0]
        self.bar_height = self.rect_y_len
        for idb, (action, color) in enumerate(self.action_color_dict.items()):
            bar_y = self.calendar_bottom - (4 + 2 * idb) * self.rect_y_len

            for ida, row in self.df.iterrows():
                bar_x = ida * self.bar_width
                rect = Rectangle(
                    (bar_x, bar_y),
                    *(self.bar_width, self.bar_height),
                    facecolor=color,
                    edgecolor="none",
                )
                if row[action]:
                    self.ax.add_patch(rect)

            outline_rect = Rectangle(
                (0, bar_y),
                *(self.calendar_right, self.bar_height),
                facecolor="none",
                edgecolor="gray",
            )
            self.ax.add_patch(outline_rect)

            plt.text(
                -self.bar_width,
                bar_y + self.bar_height / 2,
                self.data_parser.action_en_zh_dict[action],
                va="center",
                ha="right",
                fontsize=self.fontsize,
            )


calendar_plotter = CalendarPlotter()
calendar_plotter.plot()
