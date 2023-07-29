import sys
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
sys.path.append('../Thesis Practical Work')

import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import pandas as pd
import datetime as dt 

from Benchmark_strategies.RandomStrat import randomStrat
from Benchmark_strategies.regularStrat import BuyAndHold

from GUI_elements.variables import colors


def compare_returns(ticker, start_date, end_date, commission, pause, strategy1, strategy2, time, buy_signal=[0,0], sell_signal=[0,0], rsiwindow=[0,0]):

    
    price_data, equity1, ticker, *_ = strategy1(ticker, start_date, end_date, commission, pause, buy_signal[0], sell_signal[0], rsiwindow[0])
    _, equity2, *_ = strategy2(ticker, start_date, end_date, commission, pause, buy_signal[1], sell_signal[1], rsiwindow[1])

    price_data = price_data.reset_index()
    price_data = price_data.drop(price_data.index[-1])

    price_data['Strategy1'] = equity1
    price_data['Strategy2'] = equity2 

    if time=="yearly":
     price_data = price_data.groupby(price_data['Date'].dt.year).mean().reset_index()
    
    elif time=="monthly":
       price_data['year'] = price_data['Date'].dt.year
       price_data['month'] = price_data['Date'].dt.month
       price_data = price_data.groupby(['year','month']).mean().reset_index()  
       price_data['Date'] = price_data['year'].astype(str) + '-' + price_data['month'].astype(str)
   
    elif time=="daily":
     price_data = price_data.reset_index()
       
    returns1 = []
    returns2 = []
    
    for i in range(1, len(price_data), 1): 

        differential1 = round(((price_data['Strategy1'][i]-price_data.loc[i-1,'Strategy1'])/price_data.loc[i-1,'Strategy1'])*100,2)
        differential2 = round(((price_data.loc[i,'Strategy2']-price_data.loc[i-1,'Strategy2'])/price_data.loc[i-1, 'Strategy2'])*100,2)
        returns1.append(differential1)
        returns2.append(differential2)

    plot_data = pd.DataFrame({'Date': price_data['Date'][:-1], 'Strategy1': returns1, 'Strategy2': returns2})

    figure = Figure(figsize=(12, 6))
    plot = figure.add_subplot(111)

    plot.plot(plot_data['Date'], plot_data['Strategy1'], color=colors[0])
    plot.plot(plot_data['Date'], plot_data['Strategy2'], color=colors[1])

    plot.set_title('Returns (%) comparison: ' + str(strategy1.__name__) + " Vs " + str(strategy2.__name__) + " on " +ticker, fontweight="bold")
    plot.set_xlabel('Date', fontweight="bold")
    plot.set_ylabel(str(time)+' return (%)', fontweight="bold")

    plot.legend([str(strategy1.__name__), str(strategy2.__name__), ticker + 'returns'], loc='upper left')
    plot.set_ylim(ymax=max(plot_data['Strategy1'].max()*1.5, plot_data['Strategy2'].max()) * 1.5)
    plot.xaxis.set_major_locator(plt.MaxNLocator(5))


    return figure, plot_data


if __name__=="__main__":

    compare_returns("KO", "2000-01-01", "2023-01-01", 0.003, "2", randomStrat, BuyAndHold, "yearly", [30, 70], [2, 5], [3, 3])
    


 