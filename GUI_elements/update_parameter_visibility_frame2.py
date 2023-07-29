import tkinter as tk
from tkinter import ttk

def update_parameter_visibility2(strategy: str, h: int, buy_signal_label: tk.Label, buy_signal_combobox: ttk.Combobox, sell_signal_label: tk.Label, sell_signal_combobox: ttk.Combobox, rsiWindow_label=0, rsiWindow_box=0):

    if strategy == "RSI + MACD + EMA9" or strategy == "RSI + MACD" or strategy == "RSI":

        buy_signal_label.configure(text="Buy Signal")
        sell_signal_label.configure(text="Sell Signal")

        buy_signal_label.place(x=h, y=50)
        buy_signal_combobox.place(x=h+90, y=50)
        sell_signal_label.place(x=h, y=80)
        sell_signal_combobox.place(x=h+90, y=80)
        rsiWindow_label.place(x=h, y=110)
        rsiWindow_box.place(x=h+90, y=110)

    elif strategy == "MovingAverageCrossOver":

        rsiWindow_box.place_forget()
        rsiWindow_label.place_forget()

        buy_signal_label.configure(text="Moving avg 1")
        sell_signal_label.configure(text="Moving avg 2")

       
        buy_signal_label.place(x=h, y=50)
        buy_signal_combobox.place(x=h+90, y=50)
        sell_signal_label.place(x=h, y=80)
        sell_signal_combobox.place(x=h+90, y=80)
    

    else:
        buy_signal_label.place_forget()
        buy_signal_combobox.place_forget()
        sell_signal_label.place_forget()
        sell_signal_combobox.place_forget()
        rsiWindow_box.place_forget()
        rsiWindow_label.place_forget()
