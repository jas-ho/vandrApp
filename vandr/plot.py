import sys
sys.path.append("../")
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns
from vandr.database import *


def analyse_donations(spenden, today):
    s = spenden.sort_values('pay_date')
    s['Gesammelte Spenden vandr'] = s["amount"].cumsum()
    p = s.drop_duplicates('pay_date', keep='last')
    # copy last day point to fill data up to the very present
    if not today in p.pay_date:
        p = p.append({"pay_date": today, 'Gesammelte Spenden vandr': p['Gesammelte Spenden vandr'].max()},
                     ignore_index=True)
    return p

def plot_donations(sp_df, today, last_week):
    fig, ax = plt.subplots(figsize=(6, 4))
    sp_df.plot(ax=ax, y='Gesammelte Spenden vandr', x="pay_date", rot=70)
    ax.set_ylabel("Euro", fontsize=14)
    ax.set_xlabel("")
    ax.tick_params(axis='both', which='major', labelsize=13)
    ax.set_xlim(last_week, today)
    fig.tight_layout()
    return fig, ax

def analyse_users(rawData):
    rawData['day'] = pd.to_datetime(pd.to_datetime(rawData["created"]).dt.date)
    rawData['cnt'] = 1
    #new_columns = rawData.columns.values
    #new_columns[1] = 'User'
    #rawData.columns = new_columns
    rawData = rawData[['day', 'cnt', 'nickname']]
    # Collapse and count number of instances by day
    aggData = rawData.groupby(['day']).count()
    # To fill voids reindex collapsed data with a list of dates
    idx = pd.date_range('15/08/2016', dt.datetime.today().strftime("%d/%m/%Y"))
    aggData = aggData.reindex(idx, fill_value=0)
    aggData['tot_members'] = aggData['cnt'].cumsum()
    aggData.reset_index()
    return aggData

def plot_user_number(aggData, today, last_week):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(aggData.index, aggData.tot_members, lw=2)
    plt.xticks(rotation=70)
    ax.set_ylabel("Users")
    # force interger y label
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_ylim(-0.1, aggData.tot_members.max())
    ax.set_xlim(last_week, today)
    ax.tick_params(axis='both', which='major', labelsize=13)
    fig.tight_layout()
    return fig, ax


def main():
    # donations over time
    beginning_of_time= dt.date(2016,8,15)
    d = Donation.query
    donations_df = pd.read_sql(d.statement, d.session.bind)
    today = dt.date.today()
    last_week = today - dt.timedelta(days=today.weekday(), weeks=1)
    sp_df = analyse_donations(donations_df, today)
    print (sp_df['amount'].sum())
    fig, ax = plot_donations(sp_df, today, beginning_of_time)
    fig.savefig("./static/images/spenden_cum.png")

    # get active user count over time
    q = User.query.filter(User.active == True)
    df = pd.read_sql(q.statement, q.session.bind)
    print (df)
    agg_user = analyse_users(df)
    fig, ax = plot_user_number(agg_user, today, beginning_of_time)
    fig.savefig("./static/images/users_cum.png")

if __name__ == '__main__':
    main()