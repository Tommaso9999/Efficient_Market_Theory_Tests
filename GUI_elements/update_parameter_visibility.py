import tkinter as tk
from tkinter import ttk

def update_parameter_visibility(strategy: str, row: int, column: int, buy_signal_label: tk.Label, buy_signal_combobox: ttk.Combobox, sell_signal_label: tk.Label, sell_signal_combobox: ttk.Combobox, signals=0, signals_box=0, rsiWindow_label=0, rsiWindow_box=0):

    if strategy == "RSI + MACD + EMA9" or strategy == "RSI + MACD" or strategy == "RSI":
        buy_signal_label.grid(row=row, column=column, sticky="w", pady=(10, 0))
        buy_signal_combobox.grid(row=row, column=column+1, sticky="w", pady=(10, 0))
        sell_signal_label.grid(row=row+1, column=column, sticky="w", pady=(10, 0)),
        sell_signal_combobox.grid(row=row+1, column=column+1, sticky="w", pady=(10, 0))
        signals.grid(row=row-1, column=column, sticky="w", pady=(10, 0))
        signals_box.grid(row=row-1, column=column+1, sticky="w", pady=(10, 0))
        rsiWindow_label.grid(row=row+2, column=column, sticky="w", pady=(10,0))
        rsiWindow_box.grid(row=row+2, column=column+1, sticky="w", pady=(10,0))
  
    else:
        buy_signal_label.grid_forget()
        buy_signal_combobox.grid_forget()
        sell_signal_label.grid_forget()
        sell_signal_combobox.grid_forget()
        signals.grid_forget()
        signals_box.grid_forget()
        rsiWindow_box.grid_forget()
        rsiWindow_label.grid_forget()
