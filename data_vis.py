# %%
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd
# df['日期'] = pd.to_datetime(df['日期'])
df = pd.read_csv('data.csv')
# x = pd.Series(['2022-04-23'])
# x = pd.to_datetime(x)
# print(x)
df['日期'] = pd.to_datetime(df['日期'])
# print(df['日期'])
# print(df)
print(df.info())

fig, ax = plt.subplots()
ax.add_patch(Rectangle((1, 1), 1, 1))
ax.add_patch(Rectangle((2, 2), 1, 1))
ax.plot()
# plt.show()
