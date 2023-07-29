
import sys
sys.path.append('../Thesis Practical Work')

import yfinance as yf 
import datetime as dt 
import matplotlib.pyplot as plt 
import pandas as pd 
import matplotlib.ticker as ticker 
import random 
import datetime as dt 
import ta 


def MovingAverageCrossOver(ticker, start_date, end_date, commission, pause, moving_average1=50, moving_average2=200, *args, **kwargs):

    pause = int(pause)

    sp500_data = yf.download(ticker, start=start_date, end=end_date)
    current = sp500_data['Close'].iloc[0]
    equity = [current]
    action = "buy"
    operations_time_day=0

    sma50 = sp500_data['Close'].rolling(moving_average1).mean()
    sma200 = sp500_data['Close'].rolling(moving_average2).mean()

    sp500_data["SMA50"] = sma50
    sp500_data["SMA200"] = sma200


    for k in range(1, len(sp500_data.index)-1):
        
        previous = action
        prev = sp500_data['Close'].iloc[k]
        current = sp500_data['Close'].iloc[k+1]
        differential_percentage = 1+((current - prev) / prev)

        #variants, extra rules  sp500_data.iloc[k-1]['SMA50']<sp500_data.iloc[k-1]['SMA200']
        # sp500_data.iloc[k-1]['SMA50']>sp500_data.iloc[k-1]['SMA200'] and 

        buy = sp500_data.iloc[k]['SMA50']>sp500_data.iloc[k]['SMA200'] and action=="sell" and operations_time_day>pause
        sell = sp500_data.iloc[k]['SMA50']<sp500_data.iloc[k]['SMA200'] and action=="buy" and operations_time_day>pause

        if buy:
            action = "buy"
            operations_time_day=0
        
        if sell:
            action = "sell"
            operations_time_day=0
        
        if action=="buy": 
            equity.append(equity[-1]*differential_percentage)

        if action=="sell" and previous==action:
            equity.append(equity[-1])
        
        if action=="sell" and previous!=action: 
            equity.append(equity[-1]*(1-commission))

    

        operations_time_day +=1 
    
    return sp500_data, equity, ticker, moving_average1, moving_average2, pause, *args


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.figure import Figure
import pandas as pd
import matplotlib.pyplot as plt


def plotting_moving_average_crossover(sp500_data, equity, tickerr, movingavg1, movingavg2, showsignals, pause, *args, **kwargs):


    fig = Figure(figsize=(12, 6))
  

    axs = fig.subplots(2)


    axs[0].plot(sp500_data.index[:-1], equity, label='Equity', color="blue")  # Plot equity line
    axs[0].plot(sp500_data.index[:-1], sp500_data['Close'][:-1], label=tickerr, color="red")  # Plot equity line
    axs[1].plot(sp500_data.index[:-1], sp500_data['SMA50'][:-1], label='Moving Avg 50', color="red")  # Plot moving avg 50 line
    axs[1].plot(sp500_data.index[:-1], sp500_data['SMA200'][:-1], label='Moving Avg 200', color="green")  # Plot moving avg 200 line

    axs[0].set_xlabel('Time')  # Set x-axis label
    axs[0].set_ylabel('Value')  # Set y-axis label
    axs[0].set_title('Moving Average Crossover')  # Set title

    axs[0].spines['top'].set_visible(False)
    axs[0].spines['right'].set_visible(False)
    
    axs[1].spines['top'].set_visible(False)
    axs[1].spines['right'].set_visible(False)

    axs[0].legend(loc='upper left') 
    axs[1].legend(loc='upper left')

    action = "buy"
    operations_time_day = 0

    for k in range(1, len(sp500_data.index) - 1):

        buy = sp500_data.iloc[k]['SMA50']>sp500_data.iloc[k]['SMA200'] and action=="sell" and operations_time_day>pause
        sell = sp500_data.iloc[k]['SMA50']<sp500_data.iloc[k]['SMA200'] and action=="buy" and operations_time_day>pause


        if buy:
            action = "buy"
            operations_time_day = 0
            axs[0].axvline(x=sp500_data.index[k], color='green', alpha=1, ymin=0, ymax=1)
            axs[1].axvline(x=sp500_data.index[k], color='green', alpha=1, ymin=0, ymax=1)


        if sell:
            action = "sell"
            operations_time_day = 0
            axs[0].axvline(x=sp500_data.index[k], color='red', alpha=1, ymin=0, ymax=1)
            axs[1].axvline(x=sp500_data.index[k], color='red', alpha=1, ymin=0, ymax=1)
           

        operations_time_day += 1

    return fig

if __name__=="__main__":
 
 sp500_data, equity, tickerr, movingavg1, movingavg2, pause = MovingAverageCrossOver("^GSPC", "2010-01-01", "2023-01-01",0,"2", 1, 50)
 sp500_data.index = pd.to_datetime(sp500_data.index)
 show_signals = True
 list = []
 for i in range(1, len(sp500_data)+1, 1):
     list.append(i)

 sp500_data['index'] = list
 print(sp500_data)
 sp500_data.to_csv(r'file.csv')
 plotting_moving_average_crossover(sp500_data, equity,tickerr, movingavg1, movingavg2, "True", pause)