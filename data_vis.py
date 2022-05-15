# %%
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd


class DataParser:
    def __init__(self, data_filename="data.csv"):
        self.df = pd.read_csv(data_filename)
        cols_rename_dict = {
            "日期": "date",
            "编程": "code",
            "交易": "trade",
            "健身": "body",
            "读书": "read",
        }
        self.df.rename(columns=cols_rename_dict, inplace=True)
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
        self.df = DataParser(data_filename).df

    def plot(self):
        fig, ax = plt.subplots()
        ax.set_aspect(self.aspect)
        row0 = self.df.iloc[[0]]
        wk_offset = row0["date"][0].isoweekday() - 1
        for ida, row in self.df.iterrows():
            for idb, (key, val) in enumerate(self.action_color_dict.items()):
                rect_x_len = self.aspect
                rect_y_len = 1
                rect_x = rect_x_len * ((idb % 2) + 2.5 * ((ida + wk_offset) // 7))
                rect_y = rect_y_len * ((idb // 2) - 2.5 * ((ida + wk_offset) % 7))
                facecolor = val if row[key] == 1 else "white"
                rect = Rectangle(
                    (rect_x, rect_y),
                    rect_x_len,
                    rect_y_len,
                    facecolor=facecolor,
                    edgecolor="gray",
                )
                ax.add_patch(rect)
        ax.plot()
        # plt.show()


calendar_plotter = CalendarPlotter()
calendar_plotter.plot()
