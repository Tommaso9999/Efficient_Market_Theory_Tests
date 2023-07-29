
import sys
sys.path.append('../Thesis Practical Work')

from datetime import datetime, timedelta
from ta_strategies.RSI_MACD_EMA9 import RSIMACDEma9, plotting_ema9
from ta_strategies.RSI_MACD_NoEMA9 import RSIMACDNoEma9, plotting_noEma9
from ta_strategies.RSI import RSIStrat, plotting_rsi
from Benchmark_strategies.RandomStrat import randomStrat, plotting_random
from Benchmark_strategies.regularStrat import BuyAndHold, plotting_regular
from ta_strategies.Moving_average_crossover import MovingAverageCrossOver, plotting_moving_average_crossover

current_date = datetime.now()
one_day_ago = current_date - timedelta(days=1)
date_string = one_day_ago.strftime('%Y-%m-%d')

hex = ["#FFB6C1", "#87CEEB"]

colors = [
    "#FF0000",  # red
    "#4169E1",  # Blue
]


strategies = {
    
            "MovingAverageCrossOver": {
                "function": MovingAverageCrossOver,
                "plotting_function": plotting_moving_average_crossover
            },
            "RSI + MACD + EMA9": {
                "function": RSIMACDEma9,
                "plotting_function": plotting_ema9
            },
            "RSI + MACD": {
                "function": RSIMACDNoEma9,
                "plotting_function": plotting_noEma9
            },
            "RSI": {
                "function": RSIStrat,
                "plotting_function": plotting_rsi
            },
            "Random": {
                "function": randomStrat,
                "plotting_function": plotting_random
            },
            "Buy & Hold": {
                "function": BuyAndHold,
                "plotting_function": plotting_regular
            }
        }
