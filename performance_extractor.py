import sys
sys.path.append('../Thesis Practical Work')
import json
import pandas as pd 
from GUI_elements.variables import strategies
import yfinance as yf 
import numpy as np 

from Benchmark_strategies.regularStrat import BuyAndHold


commission = 0.003
time = "yearly"

dates = [["2010-01-01", "2023-01-01"], ["2000-01-01","2010-01-01"], ["1990-01-01","2000-01-01"], ["1980-01-01","1990-01-01"]]
pause_windows = [0, 1, 5, 10, 100]

def get_strat_returns(ticker, start_date, end_date, commission, pause, strategy1, strategy2):

    sp500_data = yf.download(ticker, start=start_date, end=end_date)
    mean = "none"
    mean2 = "none"

    if len(sp500_data['Close'])>360:

        if strategy1.__name__ =="MovingAverageCrossOver":
         price_data, equity1, *_ = strategy1(ticker, start_date, end_date, commission, pause, 50, 200, 14)
         print("KAAAAAA")
        else:
         price_data, equity1, *_ = strategy1(ticker, start_date, end_date, commission, pause, 30, 70, 14)
         print("Not KAA")
        
        price_data2, equity2, *_ = strategy2(ticker, start_date, end_date, commission, pause, 30, 70, 14)

        price_data = price_data.reset_index()
        price_data = price_data.drop(price_data.index[-1])

        price_data2 = price_data2.reset_index()
        price_data2 = price_data2.drop(price_data2.index[-1])

        price_data['Strategy1'] = equity1
        price_data2['Strategy2'] = equity2

        price_data = price_data.groupby(price_data['Date'].dt.year).mean().reset_index()
        price_data2 = price_data2.groupby(price_data2['Date'].dt.year).mean().reset_index()
       
        returns1 = []
        returns2 = []
    
        for i in range(1, len(price_data), 1): 
            differential1 = round(((price_data['Strategy1'][i]-price_data.loc[i-1,'Strategy1'])/price_data.loc[i-1,'Strategy1'])*100,2)
            returns1.append(differential1)

            differential2 = round(((price_data2['Strategy2'][i]-price_data2.loc[i-1,'Strategy2'])/price_data2.loc[i-1,'Strategy2'])*100,2)
            returns2.append(differential2)

        plot_data = pd.DataFrame({'Date': price_data['Date'][:-1], 'Strategy1': returns1, 'buy&hold': returns2})
        mean = plot_data['Strategy1'].mean()
        mean2 = plot_data['buy&hold'].mean()
 
    return mean, mean2


with open(r'../compare_markets/tickers.json') as file:
    tickers = json.load(file)

strategy_results = []


for pause in pause_windows:
 for date in dates:
  for strat in strategies:
    if strat=="Buy & Hold":
       continue 

    for item in tickers["S&P 500"]:
        belonging_market = "-"
        for market in tickers: 
           if item in tickers[market]:
              belonging_market = market 
        
        strat_performance, asset_performance = get_strat_returns(item, date[0], date[1], commission,pause, strategies[strat]['function'], BuyAndHold)
     

        if strat_performance !="none":

            strategy_results.append({
                "strategy": strat,
                "ticker":item,
                "time window": date[0]+"/"+date[1],
                "commission": str(commission*100),
                "market": belonging_market,
                "pause window (days)": pause,
                "yearly avg performance strategy (%)": strat_performance,
                "yearly avg performance buy & hold (%)": asset_performance,
                "yearly return differential (%)": strat_performance-asset_performance,
            })
            
df = pd.DataFrame(strategy_results)
df.to_csv(r'../compare_markets/strategies_comparisons_results/ANOTHER_ONE.csv')


