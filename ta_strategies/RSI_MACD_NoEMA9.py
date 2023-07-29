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



def RSIMACDNoEma9(ticker, start_date, end_date, commission, pause, buy_signal, sell_signal, rsiWindow):

    pause = int(pause)

    sp500_data = yf.download(ticker, start=start_date, end=end_date)
    current = sp500_data['Close'].iloc[0]
    equity = [current]
    action = "buy"
    operations_time_day=0

    # Compute the RSI index
    rsi = ta.momentum.RSIIndicator(sp500_data['Close'], window=rsiWindow)
    sp500_data['RSI'] = rsi.rsi()

    #compute the MACD indicator
    macd = ta.trend.MACD(sp500_data['Close'])
    sp500_data['MACD'] = macd.macd()

    # Loop through the data and simulate the bot's behavior. in this case we have RSI with 30,50,70 configuration + MACD 0 cross configuration. 
    for k in range(1, len(sp500_data.index)-1):
        
        previous = action
        prev = sp500_data['Close'].iloc[k]
        current = sp500_data['Close'].iloc[k+1]
        differential_percentage = 1+((current - prev) / prev)

        #RSI RULES
        rsi30crossbuy = sp500_data.iloc[k-1]['RSI']<buy_signal and sp500_data.iloc[k]['RSI']>buy_signal and operations_time_day>pause and action=="sell"
        rsi70crossell = sp500_data.iloc[k-1]['RSI']>sell_signal and sp500_data.iloc[k]['RSI']<sell_signal and operations_time_day>pause and action=="buy"
        rsi50crossbuy = sp500_data.iloc[k-1]['RSI']<50 and sp500_data.iloc[k]['RSI']>50 and operations_time_day>pause and action=="sell"
        rsi50crosssell= sp500_data.iloc[k-1]['RSI']>50 and sp500_data.iloc[k]['RSI']<50 and operations_time_day>pause and action=="buy"

        #MACD RULES
        macd0crossbuy = sp500_data.iloc[k-1]['MACD']<0 and sp500_data.iloc[k]['MACD']>0 and operations_time_day>pause and action=="sell"
        macd0crosssell = sp500_data.iloc[k-1]['MACD']>0 and sp500_data.iloc[k]['MACD']<0 and operations_time_day>pause and action=="buy"

        if rsi30crossbuy or macd0crossbuy or rsi50crossbuy:
            action = "buy"
            operations_time_day=0
        

        if rsi70crossell or macd0crosssell or rsi50crosssell:
            action = "sell"
            operations_time_day=0
        
        if action=="buy": 
            equity.append(equity[-1]*differential_percentage)

        if action=="sell" and previous==action:
            equity.append(equity[-1])
        
        if action=="sell" and previous!=action: 
            equity.append(equity[-1]*(1-commission))

        

        operations_time_day +=1 
    
    return sp500_data, equity, ticker, buy_signal, sell_signal, rsiWindow, pause




import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg




def plotting_noEma9(sp500_data, equity, index, buy_signal, sell_signal, show_signals, rsiWindow, pause):
    plot_data = pd.DataFrame({'Date': sp500_data.index[:-1], 'Equity': equity})

    fig = Figure(figsize=(8, 6))


    ax1 = fig.add_subplot(311)
    ax2 = fig.add_subplot(312)
    ax3 = fig.add_subplot(313)

    fig.suptitle('Equity Growth ' + index + ' with Trading Bot Technique:\n RSI with (' + str(buy_signal) + "," + str(sell_signal) + ') &' + str(rsiWindow) + ' days configuration  +MACD', fontweight="bold", fontsize=16)

    ax1.plot(plot_data['Date'], plot_data['Equity'])
    ax1.plot(sp500_data['Close'], label=index + ' Close', color='red')
    ax1.text(sp500_data.index[-1], plot_data['Equity'].iloc[-1], 'Equity', ha='left', va='bottom')
    ax1.text(sp500_data.index[-1], sp500_data['Close'].iloc[-1], index + ' price', ha='left', va='bottom', color='red')
    ax1.legend(['Equity', index + ' Close'], loc='upper left')
    ax1.set_ylim(0, max(sp500_data['Close'].max(), plot_data['Equity'].max()) * 1.2)

    ax2.plot(sp500_data.index, sp500_data['RSI'], color='purple')
    ax2.plot(sp500_data.index, [sell_signal] * len(sp500_data['RSI']), color="red", linewidth=0.7)
    ax2.plot(sp500_data.index, [buy_signal] * len(sp500_data['RSI']), color="green", linewidth=0.7)
    ax2.plot(sp500_data.index, [50] * len(sp500_data['RSI']), color="black", linewidth=0.7)
    ax2.legend(['RSI'], loc='upper left')
    ax2.set_ylim(0, sp500_data['RSI'].max() * 1.2)

    ax3.plot(sp500_data.index, sp500_data['MACD'], color='orange')
    ax3.plot(sp500_data.index, [0] * len(sp500_data['RSI']), color="black", linewidth=0.7)
    ax3.legend(['MACD'], loc='upper left')
    ax3.set_ylim(sp500_data['MACD'].min() * 1.7, sp500_data['MACD'].max() * 1.7)

    for ax in [ax1, ax2, ax3]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    action = "buy"
    operations_time_day = 0

    if show_signals:
        for k in range(1, len(sp500_data.index) - 1):
            rsi30crossbuy = (
                sp500_data.iloc[k - 1]['RSI'] < buy_signal and
                sp500_data.iloc[k]['RSI'] > buy_signal and
                operations_time_day > pause and
                action == "sell"
            )
            rsi70crossell = (
                sp500_data.iloc[k - 1]['RSI'] > sell_signal and
                sp500_data.iloc[k]['RSI'] < sell_signal and
                operations_time_day > pause and
                action == "buy"
            )
            rsi50crossbuy = (
                sp500_data.iloc[k - 1]['RSI'] < 50 and
                sp500_data.iloc[k]['RSI'] > 50 and
                operations_time_day > pause and
                action == "sell"
            )
            rsi50crosssell = (
                sp500_data.iloc[k - 1]['RSI'] > 50 and
                sp500_data.iloc[k]['RSI'] < 50 and
                operations_time_day > pause and
                action == "buy"
            )
            macd0crossbuy = (
                sp500_data.iloc[k - 1]['MACD'] < 0 and
                sp500_data.iloc[k]['MACD'] > 0 and
                operations_time_day > pause and
                action == "sell"
            )
            macd0crosssell = (
                sp500_data.iloc[k - 1]['MACD'] > 0 and
                sp500_data.iloc[k]['MACD'] < 0 and
                operations_time_day > pause and
                action == "buy"
            )

            if rsi30crossbuy:
                action = "buy"
                operations_time_day = 0
                ax1.axvline(x=sp500_data.index[k], color='green', alpha=1, ymin=0, ymax=1)
                ax2.scatter(sp500_data.index[k], buy_signal, s=250, color='green', alpha=1, linewidth=2, facecolor='none')

            if rsi70crossell:
                action = "sell"
                operations_time_day = 0
                ax1.axvline(x=sp500_data.index[k], color='red', alpha=1, ymin=0, ymax=1)
                ax2.scatter(sp500_data.index[k], sell_signal, s=250, color='red', alpha=1, linewidth=2, facecolor='none')

            if macd0crossbuy:
                action = "buy"
                operations_time_day = 0
                ax1.axvline(x=sp500_data.index[k], color='green', alpha=1, ymin=0, ymax=1)
                ax3.scatter(sp500_data.index[k], 0, s=250, color='green', alpha=1, linewidth=2, facecolor='none')

            if macd0crosssell:
                action = "sell"
                operations_time_day = 0
                ax1.axvline(x=sp500_data.index[k], color='red', alpha=1, ymin=0, ymax=1)
                ax3.scatter(sp500_data.index[k], 0, s=250, color='red', alpha=1, linewidth=2, facecolor='none')

            if rsi50crossbuy:
                action = "buy"
                operations_time_day = 0
                ax1.axvline(x=sp500_data.index[k], color='green', alpha=1, ymin=0, ymax=1)
                ax2.scatter(sp500_data.index[k], 50, s=250, color='green', alpha=1, linewidth=2, facecolor='none')

            if rsi50crosssell:
                action = "sell"
                operations_time_day = 0
                ax1.axvline(x=sp500_data.index[k], color='red', alpha=1, ymin=0, ymax=1)
                ax2.scatter(sp500_data.index[k], 50, s=250, color='red', alpha=1, linewidth=2, facecolor='none')

            operations_time_day += 1

 
    return fig



if __name__=="__main__":
 
 sp500_data, equity, buy_signal, sell_signal, tickerr, rsiWindow, pause = RSIMACDNoEma9("^GSPC", "2010-01-01", "2023-01-01", 0.003, "2", 30, 70, 14)
 sp500_data.index = pd.to_datetime(sp500_data.index)
 show_signals = True
 plotting_noEma9(sp500_data, equity, buy_signal, sell_signal, tickerr, show_signals, rsiWindow, pause)