import pandas as pd
from tkinter import messagebox
from GUI_elements.variables import strategies


def run_strategy(ticker, start_date, end_date,commission,pause, strategy, buy_signal=0, sell_signal=0, show_signals=0, rsiWindow=0):

        if strategy in strategies:
            strategy_info = strategies[strategy]
            strategy_func = strategy_info["function"]
            plotting_func = strategy_info["plotting_function"]
            sp500_data, equity, ticker, buy_signal, sell_signal, rsiWindow, pause2 = strategy_func(ticker, start_date, end_date, commission, pause, buy_signal, sell_signal, rsiWindow)
            sp500_data.index = pd.to_datetime(sp500_data.index)
            figure = plotting_func(sp500_data, equity,ticker, buy_signal, sell_signal, show_signals, rsiWindow, pause2)

            return figure 
        
        else:
            messagebox.showerror("Error", "Invalid strategy selected.")
            return