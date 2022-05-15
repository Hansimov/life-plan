# %%
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd

df = pd.read_csv("data.csv")
cols_rename_dict = {
    "日期" : "date"     ,
    "编程" : "code"     ,
    "交易" : "trade"    ,
    "健身" : "bodybuild",
    "读书" : "read"     ,
}
df.rename(columns=cols_rename_dict, inplace=True)
df["date"] = pd.to_datetime(df["date"])

fig, ax = plt.subplots()
ax.set_aspect(1)

for idx, row in df.iterrows():
    weekday = row["date"].isoweekday()
    ax.add_patch(Rectangle((2 * idx, weekday), 1, 1, color="blue"))
ax.plot()
# plt.show()
