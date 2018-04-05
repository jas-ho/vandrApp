# http://stackoverflow.com/questions/17232683/creating-tables-in-matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_table(df, fn, fig_ax=None):

    if not fig_ax:
       fig, ax = plt.subplots(figsize=(4,4))
       #ax = fig.add_subplot(111)
       ax.xaxis.set_visible(False)
       ax.yaxis.set_visible(False)
       ax.axis('off')
    else:
         fig, ax = fig_ax
    
    ax.table(cellText=df.values, colWidths = [0.2]*len(df.columns),
             rowLabels=df.index,
             colLabels=df.columns, cellLoc = 'center', rowLoc = 'center',
             loc='center')
    fig.savefig(fn)
