import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

import seaborn as sns
import numpy as np
from matplotlib.ticker import MaxNLocator
from plot_table import plot_table

# Import csv
rawData = pd.read_csv('VANDR inscriptions.csv')

# Keep only important data: the date (without time) and a counter
rawData['day'] = pd.to_datetime(pd.to_datetime(rawData.Timestamp).dt.date)
rawData['cnt'] = 1
new_columns = rawData.columns.values
new_columns[1] = 'User'
rawData.columns = new_columns
#rawData.rename({'Such dir einen Nickname aus:' : "User"})
rawData = rawData[['day','cnt', 'User']]

# Collapse and count number of instances by day
aggData = rawData.groupby(['day']).count()

# To fill voids reindex collapsed data with a list of dates
idx = pd.date_range('15/08/2016', dt.datetime.today().strftime("%d/%m/%Y"))
aggData = aggData.reindex(idx, fill_value=0)

# The running sum tells us the number of members per day
aggData['tot_members'] = aggData['cnt'].cumsum()
aggData.reset_index()

# Do the plotting (the graph is ugly, to be improved)
fig, ax  = plt.subplots(figsize=(5,3))
ax.plot(aggData.index, aggData.tot_members, lw=2)
plt.xticks(rotation=70)

ax.set_ylabel("Users")
# force interger y label
ax.yaxis.set_major_locator(MaxNLocator(integer=True))

ax.set_ylim(-0.1,aggData.tot_members.max())
fig.tight_layout()
fig.savefig('users.png')

# my plotting function performs poorly
#plot_table(rawData[['User', "day"]], 'test_table.pdf')

t = rawData[['User', "day"]]
t.to_pickle("table.p")
t.to_csv("table.csv")
#t.to_html("../static/table.html")
