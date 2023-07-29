import sys
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd

sys.path.append('../Thesis Practical Work')

import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import pandas as pd
import datetime as dt 


from scipy.stats import wilcoxon
from Benchmark_strategies.RandomStrat import randomStrat
from Benchmark_strategies.regularStrat import BuyAndHold
from pingouin import compute_effsize

from GUI_elements.variables import hex



def a12_paired(lst1, lst2):
 more = same = 0.0
 for i in range(len(lst1)):
    if lst1[i] == lst2[i]:
        same += 1
    elif lst1[i] > lst2[i]:
        more += 1
 return (more + 0.5*same) /len(lst1)



def compare_returns_grid(data, strategy1, strategy2):
 
    figure = plt.figure(figsize=(6, 6))
    gs = gridspec.GridSpec(5, 3, figure=figure) 

    axes = [
        plt.subplot(gs[0, 0]),
        plt.subplot(gs[0, 1]),
        plt.subplot(gs[0, 2]),
        plt.subplot(gs[1, 0]),
        plt.subplot(gs[1, 1]),
        plt.subplot(gs[1, 2]),
        plt.subplot(gs[2, 0]),
        plt.subplot(gs[2, 1]),
        plt.subplot(gs[2, 2]),
        plt.subplot(gs[3, :]),
        plt.subplot(gs[4, :])   
    ]

    axes[0].text(0.5, 0.5, 'Strategy', fontsize=12, ha='center')
    axes[1].text(0.5, 0.5, strategy1.__name__, fontsize=12, ha='center')
    axes[2].text(0.5, 0.5, strategy2.__name__, fontsize=12, ha='center')
    axes[3].text(0.5, 0.5, 'Average '+ ' return (%)', fontsize=12, ha='center')
    axes[4].text(0.5, 0.5, round(data['Strategy1'].mean(),3), fontsize=12, ha='center')
    axes[5].text(0.5, 0.5, round(data['Strategy2'].mean(),3), fontsize=12, ha='center')
    axes[6].text(0.5, 0.5, 'Standard Deviation', fontsize=12, ha='center')
    axes[7].text(0.5, 0.5, round(data['Strategy1'].std(),3), fontsize=12, ha='center')
    axes[8].text(0.5, 0.5, round(data['Strategy2'].std(),3), fontsize=12, ha='center')

    indexes=[0,3,6]

    for i in indexes:
        axes[i].set_facecolor('lightgray')
    
    axes[1].set_facecolor(hex[0])
    axes[2].set_facecolor(hex[1])

    if data['Strategy1'].equals(data['Strategy2']):
     axes[9].text(0.5, 0.5, "You are comparing the same distribution with itself, cannot perform Wilcoxon or \n statistical cataclysm will arise!", ha='center', va='center')
    else:
     _, p = wilcoxon(data['Strategy1'], data['Strategy2'])
     axes[9].text(0.5, 0.5, "Wilcoxon test difference confidence: "+str(round((1-p)*100, 2))+"%", ha='center', va='center')

    A12 = a12_paired(data['Strategy1'], data['Strategy2'])

    vargah = 2 * abs(A12 - 0.5)
    ratings = {
    'extremely low': 0 <= vargah <0.05,
    'low': 0.05 <= vargah < 0.2,
    'medium': 0.2 <= vargah < 0.4,
    'high': 0.4<= vargah < 0.6,
    'extremely high': vargah>=0.6
    }

    judgment ='extremely low/no' if ratings['extremely low'] else 'low' if ratings['low'] else 'medium' if ratings['medium'] else 'high' if ratings['high'] else 'extremely high'
    axes[10].text(0.5, 0.5,"vargah delanay effect size: "+str(round(vargah,2)) +" --> "+judgment+" difference",fontsize=12, ha='center')

    for ax in axes:
       ax.set_xticks([])
       ax.set_yticks([])

    plt.close(figure)

    return figure


