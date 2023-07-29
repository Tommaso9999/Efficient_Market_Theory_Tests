import sys
sys.path.append('../Thesis Practical Work')

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def create_canvas(canvas_frame: tk.Frame, width: int, height: int, row: int, column: int, figure: Figure):
    
    canvas = FigureCanvasTkAgg(figure, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().configure(width=width, height=height)
    canvas.get_tk_widget().grid(row=row, column=column, sticky="nsew")

