import sys
import pandas as pd
from datetime import datetime, timedelta
sys.path.append('../Thesis Practical Work')

import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
import matplotlib as plt 

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import datetime as dt 
import seaborn as sns 
from Benchmark_strategies.RandomStrat import randomStrat
from Benchmark_strategies.regularStrat import BuyAndHold

from GUI_elements.variables import colors

def compare_returns_boxplot(ticker, plot_data, strategy1, strategy2, time):

    
    plot_data = plot_data.drop(columns=['Date'])
    plot_data = plot_data.rename(columns={'Strategy1': str(strategy1.__name__), 'Strategy2': str(strategy2.__name__)})

    figure = Figure(figsize=(12, 6))
    plot = figure.add_subplot(111)

  
    sns.boxplot(data=plot_data, ax=plot, palette=colors)


    plot.set_title('Returns (%) Boxplot: ' + str(strategy1.__name__) + " Vs " + str(strategy2.__name__) + " on " + ticker, fontweight="bold")
    plot.set_xlabel('Strategy', fontweight="bold")
    plot.set_ylabel(str(time)+' return (%)', fontweight="bold")

    return figure

if __name__=="__main__":
    compare_returns_boxplot("KO", "2000-01-01", "2023-01-01", randomStrat, BuyAndHold, "yearly", [30, 70], [2, 5], [3, 3])
