


import pandas as pd 


df = pd.read_csv(r'strategies_comparisons_results/sp500_strategies_results_final_correction.csv')

df = df[df['yearly avg performance strategy (%)'] != 'none']
df['yearly avg performance strategy (%)'] = df['yearly avg performance strategy (%)'].astype(float)
df['yearly avg performance buy & hold (%)'] = df['yearly avg performance buy & hold (%)'].astype(float)

df['yearly return differential (%)'] = df['yearly avg performance strategy (%)'] -df['yearly avg performance buy & hold (%)']

df.to_csv(r'strategies_comparisons_results/final.csv')