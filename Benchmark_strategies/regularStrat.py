import sys
sys.path.append('../Thesis Practical Work')

import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
from matplotlib.figure import Figure

def BuyAndHold(ticker, start_date, end_date,commission, *args, **kwargs):

    sp500_data = yf.download(ticker, start=start_date, end=end_date)
    current = sp500_data['Close'].iloc[0]
    equity = [current*1.05]

    for k in range(1, len(sp500_data.index)-1):

        prev = sp500_data['Close'].iloc[k-1]
        current = sp500_data['Close'].iloc[k]
        differential_percentage = (current - prev) / prev

        if sp500_data.index[k].day == 1:  # Invest on the first day of every month
           

            equity.append((equity[-1])*(1+differential_percentage))
        else:
            equity.append(equity[-1]*(1+differential_percentage))

    sp500_data.index = pd.to_datetime(sp500_data.index)

    return sp500_data, equity, ticker, *args
       

def plotting_regular(sp500_data, equity, ticker, *args, **kwargs):
    plot_data = pd.DataFrame({'Date': sp500_data.index[:-1], 'Equity': equity})

    fig = Figure(figsize=(12, 6))
    ax = fig.add_subplot(111)

    ax.plot(plot_data['Date'], plot_data['Equity'])
    ax.set_xlabel('Date')
    ax.set_ylabel('Equity ($)')

    ax.plot(sp500_data['Close'], label=ticker + 'Close', color='red')
    ax.ticklabel_format(style='plain', axis='y')

    ax.set_title('Equity Growth ' + ticker + ' with Trading Bot Technique:\n Buy & Hold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.legend(['Equity', ticker + ' Close'], loc='upper left')
    ax.set_ylim(ymin=0)
    ax.set_ylim(ymax=max(sp500_data['Close'].max(), plot_data['Equity'].max()) * 1.2)
    



    return fig


if __name__=="__main__":
 
 sp500_data, equity, tickers = BuyAndHold("^GSPC", "2022-01-01", "2023-01-01")
 sp500_data.index = pd.to_datetime(sp500_data.index)
 fig = plotting_regular(sp500_data, equity, tickers)
