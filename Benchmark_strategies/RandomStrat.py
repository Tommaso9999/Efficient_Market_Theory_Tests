import sys
sys.path.append('../Thesis Practical Work')

import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
import random
import datetime as dt
from matplotlib.figure import Figure



def randomStrat(ticker, start_date, end_date, commission, *args, **kwargs):
    sp500_data = yf.download(ticker, start=start_date, end=end_date)

    current = sp500_data['Close'].iloc[0]
    equity = [current]
    action = "buy"
    random.seed(int(dt.datetime.now().strftime('%Y%m%d%H%M%S')))

    # Loop through the data and simulate behaviour, in this case random trading once a month
    for k in range(1, len(sp500_data.index)-1):

        previous = action
        
        prev = sp500_data['Close'].iloc[k-1]
        current = sp500_data['Close'].iloc[k]
        differential_percentage = 1+((current - prev) / prev)

        if sp500_data.index[k].day == 1:
            action = random.choice(["buy", "sell"]) #random choice between buy and sell once a month
   

        if action=="buy": 
            equity.append(equity[-1]*differential_percentage)

        if action=="sell" and previous==action:
            equity.append(equity[-1])

        if action=="sell" and previous!=action:
            equity.append(equity[-1]*(1-commission))
    
    return sp500_data, equity, ticker, *args



def plotting_random(sp500_data, equity, tickerss, *args, **kwargs):
    plot_data = pd.DataFrame({'Date': sp500_data.index[:-1], 'Equity': equity})

    fig = Figure(figsize=(12, 6))
    ax = fig.add_subplot(111)

    ax.plot(plot_data['Date'], plot_data['Equity'])
    ax.set_title('Equity Generated by Bot')
    ax.set_xlabel('Date')
    ax.set_ylabel('Equity ($)')

    ax.ticklabel_format(style='plain', axis='y')
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax.plot(sp500_data['Close'], label='S&P 500 Close', color='red')
    ax.set_title('Equity Growth ' + tickerss + ' with Trading Bot Technique:\n RANDOM')

    ax.text(sp500_data.index[-1], plot_data['Equity'].iloc[-1], 'Equity', ha='left', va='bottom')
    ax.text(sp500_data.index[-1], sp500_data['Close'].iloc[-1], tickerss + ' Price', ha='left', va='bottom', color='red')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.legend(['Equity', tickerss + ' Price'], loc='upper left')
    ax.set_ylim(ymin=0, ymax=max(sp500_data['Close'].max(), plot_data['Equity'].max()) * 1.2)

    return fig






if __name__=="__main__":
    sp500_data, equity, tickers = randomStrat("^GSPC", "2022-01-01", "2023-01-01")
   
    plotting_random(sp500_data, equity, tickers)
    