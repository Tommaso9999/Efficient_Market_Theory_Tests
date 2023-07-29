import tkinter as tk
from tkinter import messagebox
from tkinter import StringVar
from tkinter import ttk
from tkinter import font
import matplotlib as plt 
import sys
sys.path.append('../Thesis Practical Work')

from comparisons.comparison import compareStrategies
from comparisons.returns_comparison import compare_returns
from comparisons.returns_comparison_boxplot import compare_returns_boxplot
from comparisons.comparison_grid import compare_returns_grid
from comparisons.returns_distribution import compare_returns_distributions

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import ttk

from compare_markets.compare_markets import compare_markets, compare_best

from GUI_elements.create_canvas import create_canvas
from GUI_elements.run_strategy import run_strategy
from GUI_elements.update_parameter_visibility import update_parameter_visibility
from GUI_elements.update_parameter_visibility_frame2 import update_parameter_visibility2
from GUI_elements.variables import strategies, date_string


def deselect_box(event):
    root.focus_set()


def execute_strategy():

    figure1 = Figure(figsize=(5, 2), dpi=100)
    ticker = selected_ticker.get()
    start_date = selected_start_date.get()
    end_date = selected_end_date.get()
    commission = float(selected_commission_level.get())/100
    pause = selected_pause_window_1.get()
    strategy = selected_strategy.get()
    show_signals_str = selected_show_signal.get()

    if not ticker or not start_date or not end_date:
        messagebox.showerror("Error", "Please enter all the required fields.")
        return

    show_signals = True if show_signals_str == "True" else False

    if strategy == "RSI + MACD + EMA9" or strategy == "RSI + MACD" or strategy == "RSI":
        buy_signal = int(selected_buy_signal.get())
        sell_signal = int(selected_sell_signal.get())
        rsiWindow = int(selected_rsi_window.get())
        figure1 = run_strategy(ticker, start_date, end_date,commission,pause, strategy, buy_signal, sell_signal, show_signals, rsiWindow)
    elif strategy == "Random" or strategy =="Buy & Hold":
        figure1 = run_strategy(ticker, start_date, end_date,commission,pause, strategy)
    elif strategy=="MovingAverageCrossOver":
        figure1 = run_strategy(ticker, start_date, end_date, commission,pause, strategy, 50, 200)
    else:
        messagebox.showerror("Error", "Invalid strategy selected.")

    canvas1 = FigureCanvasTkAgg(figure1, master=canvas_frame1)
    canvas1.draw()
    canvas1.get_tk_widget().configure(width=1300, height=900)
    canvas1.get_tk_widget().grid(row=0, column=3, sticky="nsew", rowspan=100)




def execute_comparison():
  
    ticker = selected_ticker2.get()
    start_date = selected_start_date2.get()
    end_date = selected_end_date2.get()
    strategy_1 = strategies[selected_strategy2.get()]['function']
    strategy_2 = strategies[selected_strategy3.get()]['function']
    time_window = selected_comparison_window.get()
    buy_signal1 = int(selected_buy_signal2.get() or 0)
    buy_signal2 = int(selected_buy_signal3.get() or 0)
    sell_signal1 = int(selected_sell_signal2.get() or 0)
    sell_signal2 = int(selected_sell_signal3.get() or 0)
    rsiWindow1 = int(selected_rsi_window2.get() or 0)
    rsiWindow2 = int(selected_rsi_window3.get() or 0)
    commission = float(selected_commission.get() or 0)/100
    pause_window = selected_pause_window_2.get()

    buy_signal = [buy_signal1, buy_signal2]
    sell_signal = [sell_signal1, sell_signal2]
    rsiWindow = [rsiWindow1, rsiWindow2]

    figure = compareStrategies(ticker, start_date, end_date, commission, pause_window, strategy_1, strategy_2, buy_signal, sell_signal, rsiWindow)
    figure2, data = compare_returns(ticker, start_date, end_date, commission, pause_window, strategy_1, strategy_2, time_window, buy_signal, sell_signal, rsiWindow)


    figure3 = compare_returns_boxplot(ticker, data, strategy_1, strategy_2, time_window)
    figure4 = compare_returns_grid(data, strategy_1, strategy_2)
    figure5 = compare_returns_distributions(data, time_window, strategy_1, strategy_2)
    
    canvas = FigureCanvasTkAgg(figure, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().configure(width=800, height=400)
    canvas.get_tk_widget().grid(row=0, column=1, sticky="nsew")

    canvas2 = FigureCanvasTkAgg(figure2, master=canvas_frameb)
    canvas2.draw()
    canvas2.get_tk_widget().configure(width=800, height=400)
    canvas2.get_tk_widget().grid(row=0, column=4, sticky="nsew")

    canvas3 = FigureCanvasTkAgg(figure3, master=canvas_framec)
    canvas3.draw()
    canvas3.get_tk_widget().configure(width=800, height=400)
    canvas3.get_tk_widget().grid(row=1, column=1, sticky="nsew")

    canvas4 = FigureCanvasTkAgg(figure4, master=canvas_framed)
    canvas4.draw()
    canvas4.get_tk_widget().configure(width=800, height=400)
    canvas4.get_tk_widget().grid(row=1, column=4, sticky="nsew")

    canvas5 = FigureCanvasTkAgg(figure5, master=canvas_framee)
    canvas5.draw()
    canvas5.get_tk_widget().configure(width=1600, height=600)
    canvas5.get_tk_widget().grid(row=2, column=1, sticky="nsew", columnspan=30)




#FRAME 1
root = tk.Tk()
root.title("Strategy Execution")
root.geometry("2000x2000")


notebook1 = ttk.Notebook(root)
notebook1.pack(fill="both", expand=True)

strat_frame = ttk.Frame(notebook1)

notebook1.add(strat_frame, text="Strategies Simulator")

canvas_frame1 = tk.Frame(strat_frame, width=1300, height=900)
canvas_frame1.grid(row=0, column=3, pady=(30, 0), padx=(100,0), rowspan=100)
figure1 = Figure(figsize=(5, 2), dpi=100)

canvas1 = None
create_canvas(canvas_frame1, 1300, 900, 0, 3, figure1)


buy_signal_values = [20, 25, 30, 35, 40]
sell_signal_values = [60, 65, 70, 75, 80]
rsi_windows = [7, 14, 21, 28]
strategy_values = ["RSI + MACD + EMA9", "RSI + MACD", "RSI", "Random", "Buy & Hold", "MovingAverageCrossOver"]
ticker_values = ["^GSPC", "^STOXX50E", "^N225"]
coparison_timeframes = ["daily", "monthly", "yearly"]
show_signals = [True, False]
commission_values = [0.2, 0.3, 0.5, 1, 2]
pause_values = ["0", "1", "5", "10", "100"]

#FRAME1 BUTTONS 

selected_buy_signal = StringVar(root)
selected_sell_signal = StringVar(root)
selected_ticker = StringVar(root)
selected_strategy = StringVar(root)
selected_show_signal = StringVar(root)
selected_start_date = StringVar(root)
selected_end_date = StringVar(root)
selected_rsi_window = StringVar(root)
selected_commission_level = StringVar(root)
selected_pause_window_1 = StringVar(root)


selected_buy_signal.set("30")
selected_sell_signal.set("70")
selected_ticker.set("^GSPC")
selected_strategy.set("Random")
selected_show_signal.set("True")
selected_start_date.set("2022-01-01")
selected_end_date.set(date_string)
selected_rsi_window.set("14")
selected_commission_level.set("1")
selected_pause_window_1.set("5")

ticker_label = tk.Label(strat_frame, text="Ticker:")
ticker_label.grid(row=0, column=0, sticky="w", pady=(10, 0))
ticker_combobox = ttk.Combobox(strat_frame, textvariable=selected_ticker, values=ticker_values)
ticker_combobox.grid(row=0, column=1, sticky="w", pady=(10, 0))

strategy_label = tk.Label(strat_frame, text="Strategy:")
strategy_label.grid(row=1, column=0, sticky="w", pady=(10, 0))
strategy_combobox = ttk.Combobox(strat_frame, textvariable=selected_strategy, values=strategy_values)
strategy_combobox.grid(row=1, column=1, sticky="w", pady=(10, 0))
strategy_combobox.bind("<<ComboboxSelected>>", lambda event: update_parameter_visibility(selected_strategy.get(), 7, 0, buy_signal_label, buy_signal_combobox, sell_signal_label, sell_signal_combobox, signals, signals_box, rsiWindow_label, rsiWindow_box))

commission_label = tk.Label(strat_frame, text="Commission %:")
commission_label.grid(row=2, column=0, sticky="w", pady=(10, 0))
comission_combobox = ttk.Combobox(strat_frame, textvariable=selected_commission_level, values=commission_values)
comission_combobox.grid(row=2, column=1, sticky="w", pady=(10, 0))

signals = tk.Label(strat_frame, text="Show Signals:")
signals_box = ttk.Combobox(strat_frame, textvariable=selected_show_signal, values=show_signals)

start_date_label = tk.Label(strat_frame, text="Start Date:")
start_date_label.grid(row=3, column=0, sticky="w", pady=(10, 0))
start_date_combobox = ttk.Combobox(strat_frame, textvariable=selected_start_date,values=["1980-01-01", "1990-01-01", "2000-01-01", "2010-01-01", "2020-01-01"])
start_date_combobox.grid(row=3, column=1, sticky="w", pady=(10, 0))

end_date_label = tk.Label(strat_frame, text="End Date:")
end_date_label.grid(row=4, column=0, sticky="w", pady=(10, 0))
end_date_combobox = ttk.Combobox(strat_frame, textvariable=selected_end_date,values=["1990-12-31", "2000-12-31", "2010-12-31", "2020-12-31", date_string])
end_date_combobox.grid(row=4, column=1, sticky="w", pady=(10, 0))

selected_pause_label = tk.Label(strat_frame, text="Pause (days) after trade:")
selected_pause_label.grid(row=5, column=0, sticky="w", pady=(10, 0))
selected_pause_combobox = ttk.Combobox(strat_frame, textvariable=selected_pause_window_1,values=["1", "2", "3", "5", "10"])
selected_pause_combobox.grid(row=5, column=1, sticky="w", pady=(10, 0))


buy_signal_label = tk.Label(strat_frame, text="Buy Signal:")
sell_signal_label = tk.Label(strat_frame, text="Sell Signal:")
buy_signal_combobox = ttk.Combobox(strat_frame, textvariable=selected_buy_signal, values=buy_signal_values)
sell_signal_combobox = ttk.Combobox(strat_frame, textvariable=selected_sell_signal, values=sell_signal_values)

rsiWindow_label = tk.Label(strat_frame, text="Rsi Window:")
rsiWindow_box= ttk.Combobox(strat_frame, textvariable=selected_rsi_window, values=rsi_windows)

execute_button1 = tk.Button(strat_frame, text="Execute Strategy", command=execute_strategy)
execute_button1.grid(row=10, column=0)
execute_button1.config(width=20, height=3, bg="green")


#FRAME 2

strat_frame2 = tk.Canvas(notebook1, scrollregion=(0,0, 2000, 1800))

#enable scrolling
scrolling_frame = tk.Frame(strat_frame2)
strat_frame2.create_window((0, 0), window=scrolling_frame, anchor='nw')
scrollbar = ttk.Scrollbar(strat_frame2, orient='vertical', command=strat_frame2.yview)
scrollbar.place(relx=0.99, rely=0, relheight=1)
strat_frame2.configure(yscrollcommand=scrollbar.set)
strat_frame2.pack(side='left', fill='both', expand=True)


canvas_frame = tk.Frame(scrolling_frame)
canvas_frame.grid(row=10, column=1, pady=(10, 10))
figure = Figure(figsize=(5, 2), dpi=100)
canvas = None
create_canvas(canvas_frame, 800, 400, 0, 1, figure)

canvas_frameb = tk.Frame(scrolling_frame)
canvas_frameb.grid(row=10, column=4, pady=(10, 10))
figureb = Figure(figsize=(5, 2), dpi=100)
canvasb = None
create_canvas(canvas_frameb, 800, 400, 0, 4, figureb)

canvas_framec = tk.Frame(scrolling_frame)
canvas_framec.grid(row=11, column=1, pady=(10, 10))
figurec = Figure(figsize=(5, 2), dpi=100)
canvasc = None
create_canvas(canvas_framec, 800, 400, 1, 1, figurec)

canvas_framed = tk.Frame(scrolling_frame)
canvas_framed.grid(row=11, column=4, pady=(10, 10))
figured = Figure(figsize=(5, 2), dpi=100)
canvasd = None
create_canvas(canvas_framed, 800, 400, 1, 4, figured)

canvas_framee = tk.Frame(scrolling_frame)
canvas_framee.grid(row=12, column=1, pady=(10, 10), columnspan=30)
figuree = Figure(figsize=(5, 2), dpi=100)
canvase = None
create_canvas(canvas_framee, 1600, 600, 2, 1, figuree)

#FRAME2 BUTTONS 

selected_buy_signal2 = StringVar(root)
selected_sell_signal2 = StringVar(root)
selected_ticker2 = StringVar(root)
selected_strategy2 = StringVar(root)
selected_show_signal2 = StringVar(root)
selected_start_date2 = StringVar(root)
selected_end_date2 = StringVar(root)
selected_rsi_window2 = StringVar(root)
selected_comparison_window = StringVar(root)
selected_commission = StringVar(root)
selected_pause_window_2 = StringVar(root)

selected_ticker2.set("^GSPC")
selected_buy_signal2.set("30")
selected_sell_signal2.set("70")
selected_strategy2.set("Buy & Hold")
selected_show_signal2.set("True")
selected_start_date2.set("2022-01-01")
selected_end_date2.set(date_string)
selected_rsi_window2.set("14")
selected_comparison_window.set("monthly")
selected_commission.set("1")
selected_pause_window_2.set("5")

ticker_label2 = tk.Label(scrolling_frame, text="Ticker:")
ticker_label2.grid(row=0, column=0, sticky="w", pady=(10, 0))
ticker_combobox2 = ttk.Combobox(scrolling_frame, textvariable=selected_ticker2, values=ticker_values)
ticker_combobox2.grid(row=0, column=1, sticky="w", pady=(10, 0))

comparison_window = tk.Label(scrolling_frame, text="Comparison:")
comparison_combobox2 = ttk.Combobox(scrolling_frame, textvariable=selected_comparison_window, values=coparison_timeframes)

comparison_window.grid(row=3, column=0, sticky='w', pady=(10,20))
comparison_combobox2.grid(row=3, column=1, sticky='w', pady=(10,20))

strategy_label2 = tk.Label(scrolling_frame, text="Strategy1:", foreground="red", font=font.Font(weight="bold"))
strategy_label2.place(x=300, y=10)
strategy_combobox2 = ttk.Combobox(scrolling_frame, textvariable=selected_strategy2, values=strategy_values)
strategy_combobox2.place(x=390, y=10)
strategy_combobox2.bind("<<ComboboxSelected>>", lambda event: update_parameter_visibility2(selected_strategy2.get(),300, buy_signal_label2, buy_signal_combobox2, sell_signal_label2, sell_signal_combobox2, rsiWindow_label2, rsiWindow_box2))

start_date_label2 = tk.Label(scrolling_frame, text="Start Date:")
start_date_label2.grid(row=1, column=0, sticky="w", pady=(10, 0))

start_date_combobox2 = ttk.Combobox(scrolling_frame, textvariable=selected_start_date2,
                                   values=["1980-01-01", "1990-01-01", "2000-01-01", "2010-01-01", "2020-01-01"])
start_date_combobox2.grid(row=1, column=1, sticky="w", pady=(10, 0))


end_date_label2 = tk.Label(scrolling_frame, text="End Date:")
end_date_label2.grid(row=2, column=0, sticky="w", pady=(10, 0))

end_date_combobox2 = ttk.Combobox(scrolling_frame, textvariable=selected_end_date2,
                                 values=["1990-12-31", "2000-12-31", "2010-12-31", "2020-12-31", date_string])
end_date_combobox2.grid(row=2, column=1, sticky="w", pady=(10, 0))

buy_signal_label2 = tk.Label(scrolling_frame, text="Buy Signal:")
sell_signal_label2 = tk.Label(scrolling_frame, text="Sell Signal:")

buy_signal_combobox2 = ttk.Combobox(scrolling_frame, textvariable=selected_buy_signal2, values=buy_signal_values)
sell_signal_combobox2 = ttk.Combobox(scrolling_frame, textvariable=selected_sell_signal2, values=sell_signal_values)

rsiWindow_label2 = tk.Label(scrolling_frame, text="Rsi Window:")
rsiWindow_box2= ttk.Combobox(scrolling_frame, textvariable=selected_rsi_window2, values=rsi_windows)

selected_buy_signal3 = StringVar(root)
selected_sell_signal3 = StringVar(root)
selected_strategy3 = StringVar(root)
selected_show_signal3 = StringVar(root)
selected_start_date3 = StringVar(root)
selected_end_date3 = StringVar(root)
selected_rsi_window3 = StringVar(root)


selected_buy_signal3.set("30")
selected_sell_signal3.set("70")
selected_strategy3.set("Random")
selected_show_signal3.set("True")
selected_start_date3.set("2022-01-01")
selected_end_date3.set(date_string)
selected_rsi_window3.set("14")

strategy_label3 = tk.Label(scrolling_frame, text="Strategy2:", foreground="blue", font=font.Font(weight="bold"))
strategy_label3.place(x=600, y=10)


strategy_combobox3 = ttk.Combobox(scrolling_frame, textvariable=selected_strategy3, values=strategy_values)
strategy_combobox3.place(x=690, y=10)



strategy_combobox3.bind("<<ComboboxSelected>>", lambda event: update_parameter_visibility2(selected_strategy3.get(),600, buy_signal_label3, buy_signal_combobox3, sell_signal_label3, sell_signal_combobox3, rsiWindow_label3, rsiWindow_box3))

buy_signal_label3 = tk.Label(scrolling_frame, text="Buy Signal:")
sell_signal_label3 = tk.Label(scrolling_frame, text="Sell Signal:")

buy_signal_combobox3 = ttk.Combobox(scrolling_frame, textvariable=selected_buy_signal3, values=buy_signal_values)
sell_signal_combobox3 = ttk.Combobox(scrolling_frame, textvariable=selected_sell_signal3, values=sell_signal_values)

rsiWindow_label3 = tk.Label(scrolling_frame, text="Rsi Window:")
rsiWindow_box3= ttk.Combobox(scrolling_frame, textvariable=selected_rsi_window3, values=rsi_windows)





commission_label3 = tk.Label(scrolling_frame, text="Commission(%):")
commission_label3.place(x=900, y=10)

commission_combobox3 = ttk.Combobox(scrolling_frame, textvariable=selected_commission, values=commission_values)
commission_combobox3.place(x=1020, y=10)


pause_label3 = tk.Label(scrolling_frame, text="Pause (days):")
pause_label3.place(x=900, y=50)

pause_combobox3 = ttk.Combobox(scrolling_frame, textvariable=selected_pause_window_2, values=pause_values)
pause_combobox3.place(x=1020, y=50)


execute_button = tk.Button(scrolling_frame, text="Execute Strategies", command=execute_comparison)
execute_button.place(x=1250, y=35)
execute_button.config(width=35, height=3, bg="green")


notebook1.add(strat_frame2, text="Compare Strategies")

strat_frame2.config(highlightbackground="grey")
strat_frame2.config(highlightthickness=0)


#FRAME 3

def execute_market_comparison():
  
    market = selected_market4.get()
    strategy4 = selected_strategy4.get()
    date = selected_date_range.get()
    top = selected_top.get()
    prop = selected_prop.get()
    pause = selected_pause4.get()

    compare_markets(market, strategy4, date, top, prop, pause)

    figure10 = compare_best(market, strategy4, date, top, pause)
    canvas10 = FigureCanvasTkAgg(figure10, master=scrolling_frame3)
    canvas10.draw()
    canvas10.get_tk_widget().configure(width=1600, height=600)
    canvas10.get_tk_widget().grid(row=10, column=1, sticky="nsew")

     




market_values = ["S&P500's 11 XL sectors"]
dates_values = ["1980-01-01/1990-01-01","1990-01-01/2000-01-01","2000-01-01/2010-01-01","2010-01-01/2023-01-01"]
top_values = [5, 10, "14 (keeps sectors proportions)", 15, "all"]
prop_values = [1, 5]

strat_frame3 = tk.Canvas(notebook1, scrollregion=(0,0, 2000, 1800))

#enable scrolling
scrolling_frame3 = tk.Frame(strat_frame3)
strat_frame3.create_window((0, 0), window=scrolling_frame3, anchor='nw')
scrollbar3 = ttk.Scrollbar(strat_frame3, orient='vertical', command=strat_frame3.yview)
scrollbar3.place(relx=0.99, rely=0, relheight=1)
strat_frame3.configure(yscrollcommand=scrollbar3.set)
strat_frame3.pack(side='left', fill='both', expand=True)

selected_market4 = StringVar(root)
selected_strategy4 = StringVar(root)
selected_date_range = StringVar(root)
selected_top = StringVar(root)
selected_prop = StringVar(root)
selected_pause4 = StringVar(root)

selected_market4.set("S&P500's 11 XL sectors")
selected_strategy4.set("RSI + MACD + EMA9")
selected_date_range.set("2010-01-01/2023-01-01")
selected_top.set("10")
selected_prop.set(1)
selected_pause4.set(10)

market_label = tk.Label(scrolling_frame3, text="Market:")
market_label.grid(row=0, column=0, sticky="w", pady=(10, 0))

market_box = ttk.Combobox(scrolling_frame3, textvariable=selected_market4, values=market_values)
market_box.grid(row=0, column=1, sticky="w", pady=(10, 0))

strat_label4 = tk.Label(scrolling_frame3, text="Strategy:")
strat_label4.grid(row=1, column=0, sticky="w", pady=(10, 0))

strat_box4 = ttk.Combobox(scrolling_frame3, textvariable=selected_strategy4, values=strategy_values)
strat_box4.grid(row=1, column=1, sticky="w", pady=(10, 0))

date_label_4 = tk.Label(scrolling_frame3, text="Date range:")
date_label_4.grid(row=2, column=0, sticky="w", pady=(10, 0))

date_box4 = ttk.Combobox(scrolling_frame3, textvariable=selected_date_range, values=dates_values)
date_box4.grid(row=2, column=1, sticky="w", pady=(10, 0))

selected_top_label_4 = tk.Label(scrolling_frame3, text="Top # tickers:")
selected_top_label_4.grid(row=3, column=0, sticky="w", pady=(10, 0))

date_box4 = ttk.Combobox(scrolling_frame3, textvariable=selected_top, values=top_values)
date_box4.grid(row=3, column=1, sticky="w", pady=(10, 0))

selected_prop_label_4 = tk.Label(scrolling_frame3, text="Proportions:")
selected_prop_label_4.grid(row=4, column=0, sticky="w", pady=(10, 0))

prop_box4 = ttk.Combobox(scrolling_frame3, textvariable=selected_prop, values=prop_values)
prop_box4.grid(row=4, column=1, sticky="w", pady=(10, 0))

selected_prop_label_5 = tk.Label(scrolling_frame3, text="Pause window:")
selected_prop_label_5.grid(row=5, column=0, sticky="w", pady=(10, 20))

prop_box5 = ttk.Combobox(scrolling_frame3, textvariable=selected_pause4, values=pause_values)
prop_box5.grid(row=5, column=1, sticky="w", pady=(10, 20))




canvas_frame4 = tk.Frame(scrolling_frame3)
canvas_frame4.grid(row=10, column=1, pady=(10, 10))
figure4b = Figure(figsize=(5, 2), dpi=100)
canvas4 = None
create_canvas(canvas_frame4, 1600, 600, 0, 1, figure4b)


execute_button4 = tk.Button(scrolling_frame3, text="Execute market comparison", command=execute_market_comparison)
execute_button4.place(x=350, y=25)
execute_button4.config(width=35, height=3, bg="green")


notebook1.add(strat_frame3, text="Compare Strategies on different Markets")


strat_frame3.config(highlightthickness=0)


root.bind("<FocusOut>", deselect_box)
root.mainloop()





