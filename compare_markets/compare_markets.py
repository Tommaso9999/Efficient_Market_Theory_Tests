import sys
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
sys.path.append('../Thesis Practical Work')

import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import pandas as pd
import pandas as pd
from squarify import normalize_sizes, squarify
from bokeh.plotting import figure, show
from bokeh.sampledata.sample_superstore import data
from bokeh.transform import factor_cmap
from bokeh.models import PrintfTickFormatter
from bokeh.models import Title

import ipywidgets as widgets
import math
from bokeh.models import HoverTool
from bokeh.models import ColumnDataSource


def compare_markets(market: str, strategy: str, date_range: str, top: str, proportion: int, pause):

    pause = int(pause)

    proportion_differential = int(proportion)

    if top=="all":
        top=10000
    elif top=="14 (keeps sectors proportions)":
        top = 14 
    else:
        top = int(top)

    if market == "S&P500's 11 XL sectors":
        dfo = pd.read_csv(r'strategies_comparisons_results/final.csv')
        dfo = dfo[dfo['market'] != 'S&P 500']
        dfo = dfo[dfo['strategy'] == strategy]
        dfo = dfo[dfo['time window'] == date_range]
        dfo = dfo[dfo['pause window (days)']==pause]
        dfo = dfo[["ticker", "market", "yearly return differential (%)"]] 
        min = dfo['yearly return differential (%)'].min()

        def transform(value, min_val):
            return math.pow((value+0.0001+min_val), proportion_differential)
        
        dfo['yearly return differential (%)'] = dfo['yearly return differential (%)'].apply(lambda x: transform(x, abs(min)))
        top_tickers = []
        for market in dfo['market'].unique():
            top_tickers_for_market = dfo[dfo['market'] == market].nlargest(top, 'yearly return differential (%)')['ticker'].tolist()
            top_tickers.extend(top_tickers_for_market)

        dfo =dfo[dfo['ticker'].isin(top_tickers)]
        sales_by_city = dfo.groupby(["market", "ticker"]).sum("yearly return differential (%)")
        sales_by_city = sales_by_city.sort_values(by="yearly return differential (%)").reset_index()
        sales_by_region = sales_by_city.groupby("market").sum("yearly return differential (%)").sort_values(by="yearly return differential (%)")

        def treemap(df, col, x, y, dx, dy, *, N=11):
            sub_df = df.nlargest(N, col)
            normed = normalize_sizes(sub_df[col], dx, dy)
            blocks = squarify(normed, x, y, dx, dy)
            blocks_df = pd.DataFrame.from_dict(blocks).set_index(sub_df.index)
            return sub_df.join(blocks_df, how='left').reset_index()
        
        x, y, w, h = 0, 0, 1600, 800
 
        blocks_by_region = treemap(sales_by_region, "yearly return differential (%)", x, y, w, h)
        dfs = []
        for index, (Region, Sales, x, y, dx, dy) in blocks_by_region.iterrows():
            dfo = sales_by_city[sales_by_city.market == Region]
            dfs.append(treemap(dfo, "yearly return differential (%)", x, y, dx, dy, N=top))
        blocks = pd.concat(dfs)

        def transform_value(value, min_val):
         
            return math.pow(value, 1/proportion_differential)-min_val
        
        blocks['yearly return differential (%)'] = blocks['yearly return differential (%)'].apply(lambda x: transform_value(x, abs(min)))
        blocks['fill_color'] = ['red' if diff < 0 else 'green' for diff in blocks['yearly return differential (%)']]
        blocks["ticker_text"] = blocks['ticker']
        blocks["ticker_size"] = blocks.apply(lambda row: "6pt" if row['yearly return differential (%)'] < -5  else "9pt", axis=1)

       
        tooltips = [("ticker", "@ticker"), ("strategy", strategy), ("differential", "@{yearly return differential (%)}")] if "@ticker" != "" else None
        hover_source = ColumnDataSource(blocks)
    
        p = figure(width=w, height=h, toolbar_location=None,
        x_axis_location=None, y_axis_location=None)
        p.x_range.range_padding = p.y_range.range_padding = 0
        p.grid.grid_line_color = None

        x = p.block('x', 'y', 'dx', 'dy', source=blocks, line_width=1, line_color="white", fill_alpha=0.8, fill_color='fill_color')
        p.text('x', 'y', x_offset=2, text="market", source=blocks_by_region, text_font_size="20pt", text_color="white")

        blocks["ytop"] = blocks.y + blocks.dy
        p.text('x', 'ytop', x_offset=3, y_offset=3, text="ticker_text", source=blocks,text_font_size="ticker_size", text_baseline="top", text_color="black")
        chart_title = "S&P500 best stocks by sector using " + strategy + " on date range: " +  date_range
        title = Title(text=chart_title, align="center", text_font_size="20pt")
        p.title = title

        for index, row in blocks_by_region.iterrows():
         p.rect(x=(row['x']+row['dx']/2), y=(row['y']+row['dy']/2), width=row['dx'], height=row['dy'], line_width=4, line_color="black", fill_alpha=0)

        hover = HoverTool(renderers=[x],tooltips=tooltips)
        p.add_tools(hover)


        show(p)
        

       


def compare_best(market: str, strategy: str, date_range: str, top: str, pause):
      
      pause = int(pause)
      
      if top=="all":
          top=30
      
      if market =="S&P500's 11 XL sectors":
        dfo = pd.read_csv(r'strategies_comparisons_results/final.csv')
        dfo = dfo[dfo['market'] != 'S&P 500']
        dfo = dfo[dfo['strategy'] == strategy]
        dfo = dfo[dfo['time window'] == date_range]
        dfo = dfo[dfo['pause window (days)'] == pause]

        dfo = dfo[dfo['']]
        dfo = dfo.groupby('market')['yearly return differential (%)'].mean().reset_index()
        dfo = dfo.nlargest(11, "yearly return differential (%)")
        fig, ax = plt.subplots()
        categories = dfo['market']
        heights = dfo['yearly return differential (%)']

        ax.bar(categories, heights)

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')
        plt.title(f"Top 11 XL markets by {strategy} yearly returns differential (%)", fontweight="bold")

        plt.xlabel('XL Market', fontweight="bold")  # Replace 'XL Markets' with an appropriate x-axis label
        plt.ylabel('Yearly Return Differential (%)', fontweight="bold")

        maxi = max(abs(min(heights)), abs(max(heights)))

        ax.set_ylim(maxi*-1.1, maxi*1.1)


        return fig




if __name__ == "__main__":
    compare_markets("S&P500's 11 XL sectors", "MovingAverageCrossOver","2010-01-01/2023-01-01", "all", 1, 10)
    compare_best("S&P500's 11 XL sectors", "RSI + MACD + EMA9", "2010-01-01/2023-01-01", "all", 1)