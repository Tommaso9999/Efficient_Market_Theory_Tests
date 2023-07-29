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

from GUI_elements.variables import colors

def compareStrategies(ticker, start_date, end_date, commission, pause, strategy1, strategy2, buy_signal=[0,0], sell_signal=[0,0], rsiwindow=[0,0]):

    price_data, equity1, ticker, *_ = strategy1(ticker, start_date, end_date, commission, pause, buy_signal[0], sell_signal[0], rsiwindow[0])
    _, equity2, *_ = strategy2(ticker, start_date, end_date, commission, pause, buy_signal[1], sell_signal[1], rsiwindow[1])

    plot_data = pd.DataFrame({'Date': price_data.index[:-1], 'Equity1': equity1, 'Equity2': equity2})
    start_date = plot_data['Date'].min()

    figure = Figure(figsize=(12, 6))
    plot = figure.add_subplot(111)
    plot.plot(plot_data['Date'], plot_data['Equity1'], color=colors[0])
    plot.plot(plot_data['Date'], plot_data['Equity2'], color=colors[1])

    plot.set_xlabel('Date', fontweight="bold")
    plot.set_ylabel('Equity ($)', fontweight="bold")

    plot.plot(price_data['Close'], label=ticker + ' Close', color='grey', linestyle='--', dashes=(10, 10), solid_capstyle='butt')

    plot.ticklabel_format(style='plain', axis='y')
    plot.set_title('Equity Growth: ' + str(strategy1.__name__) + " Vs " + str(strategy2.__name__) + " on " +ticker, fontweight="bold")

    plot.spines['top'].set_visible(False)
    plot.spines['right'].set_visible(False)

    plot.legend([str(strategy1.__name__), str(strategy2.__name__), ticker + ' Close'], loc='upper left')
    date_format = mdates.DateFormatter('%Y-%m-%d')
    plot.xaxis.set_major_formatter(date_format)
    x_ticks = pd.date_range(start_date, end_date, freq='D')
    num_ticks = min(len(x_ticks), 5)
    x_tick_locs = x_ticks[::len(x_ticks) // num_ticks]

    plot.set_xticks(x_tick_locs)

    plot.set_yscale('log')


    return figure



