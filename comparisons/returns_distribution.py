import sys
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import pandas as pd 
import numpy as np 


sys.path.append('../Thesis Practical Work')

from Benchmark_strategies.RandomStrat import randomStrat
from Benchmark_strategies.regularStrat import BuyAndHold

from GUI_elements.variables import colors

def compare_returns_distributions(data,time,strategy1, strategy2):

    figure = plt.figure(figsize=(12, 6))
    gs = gridspec.GridSpec(1, 2)

    strat1_data = data['Strategy1']
    strat2_data = data['Strategy2']
    
    
    ax1 = figure.add_subplot(gs[0, 0])
    sns.histplot(strat1_data, kde=True, ax=ax1, color=colors[0])
    ax1.set_title(str(time)+' returns (%) distribution of '+str(strategy1.__name__), fontweight='bold')

    ax2 = figure.add_subplot(gs[0, 1])
    sns.histplot(strat2_data, kde=True, ax=ax2, color=colors[1])
    ax2.set_title(str(time)+' returns (%) distribution of '+str(strategy2.__name__), fontweight='bold')

    plt.tight_layout()
    plt.close(figure)

    return figure


if __name__ == "__main__":

    numbers = np.random.normal(9, 1, 1000).tolist()
    time="Yearly"
    data = pd.DataFrame({'Strategy1': numbers, 'Strategy2': numbers})
    strategy1 = randomStrat
    strategy2 = BuyAndHold
    figure = compare_returns_distributions(data,time,strategy1, strategy2)
    plt.show()