# %%
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
import pandas as pd
import datetime

plt.rcParams["font.sans-serif"] = ["SimHei"]
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
            "code": "#0000FF",
            "trade": "#00FF00",
            "body": "#FF00FF",
            "read": "#FFFF00",
        }
        self.data_parser = DataParser(data_filename)
        self.df = self.data_parser.df

    def plot(self):
        fig, ax = plt.subplots(dpi=200)
        ax.set_aspect(self.aspect)

        # Plot daily blocks
        row0 = self.df.iloc[[0]]
        wk_offset = row0["date"][0].isoweekday() - 1
        rect_x_len = 1
        rect_y_len = rect_x_len / self.aspect
        for ida, row in self.df.iterrows():
            for idb, (action, color) in enumerate(self.action_color_dict.items()):
                # Plot color blocks
                rect_x = rect_x_len * ((idb % 2) + 2.5 * ((ida + wk_offset) // 7))
                rect_y = rect_y_len * ((idb // 2) - 2.5 * ((ida + wk_offset) % 7))
                facecolor = color if row[action] == 1 else "white"
                rect = Rectangle(
                    (rect_x, rect_y),
                    *(rect_x_len, rect_y_len),
                    facecolor=facecolor,
                    edgecolor="gray",
                )
                ax.add_patch(rect)

            # Plot day and month texts
            date = row["date"]
            day_text_x = rect_x + rect_x_len / 10
            day_text_y = rect_y + rect_y_len / 8
            date_text_str = f"{date.day:02}"
            plt.text(day_text_x, day_text_y, date_text_str)

            if date.isoweekday() == 7:
                month_text_x = rect_x
                month_text_y = rect_y - rect_y_len * 2
                month_text_str = f"{date.month}"
                # month_text_str = date.strftime("%b")
                plt.text(month_text_x, month_text_y, month_text_str, ha="center")

        # Plot legends
        handles = []
        for idb, (action, color) in enumerate(self.action_color_dict.items()):
            patch = Patch(color=color, label=self.data_parser.action_en_zh_dict[action])
            handles.append(patch)
        plt.legend(handles=handles, bbox_to_anchor=(1.05, 1))

        ax.axis("off")
        ax.plot()
        # plt.show()
        plt.savefig("calendar.png")


calendar_plotter = CalendarPlotter()
calendar_plotter.plot()
