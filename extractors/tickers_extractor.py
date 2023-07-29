

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd 

url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table', {'class': 'wikitable sortable'})
tickers = []

for row in table.findAll('tr')[1:]:
    ticker = row.findAll('td')[0].text.strip()
    tickers.append(ticker)




xlp_tickers = pd.read_csv(r'../extractors/XLP.csv')[pd.read_csv(r'../extractors/XLP.csv').iloc[:, 0] != "Symbol"].iloc[:, 0].tolist()

xlu_tickers =  pd.read_csv(r'../extractors/XLU.csv')[pd.read_csv(r'../extractors/XLU.csv').iloc[:, 0] != "Symbol"].iloc[:, 0].tolist()

xlk_tickers =  pd.read_csv(r'../extractors/XLK.csv')[pd.read_csv(r'../extractors/XLK.csv').iloc[:, 0] != "Symbol"].iloc[:, 0].tolist()

xly_tickers =  pd.read_csv(r'../extractors/XLY.csv')[pd.read_csv(r'../extractors/XLY.csv').iloc[:, 0] != "Symbol"].iloc[:, 0].tolist()

xlv_tickers =  pd.read_csv(r'../extractors/XLV.csv')[pd.read_csv(r'../extractors/XLV.csv').iloc[:, 0] != "Symbol"].iloc[:, 0].tolist()

xlc_tickers =  pd.read_csv(r'../extractors/XLC.csv')[pd.read_csv(r'../extractors/XLC.csv').iloc[:, 0] != "Symbol"].iloc[:, 0].tolist()

xlre_tickers =  pd.read_csv(r'../extractors/XLRE.csv')[pd.read_csv(r'../extractors/XLRE.csv').iloc[:, 0] != "Symbol"].iloc[:, 0].tolist()

xlf_tickers =  pd.read_csv(r'../extractors/XLF.csv')[pd.read_csv(r'../extractors/XLF.csv').iloc[:, 0] != "Symbol"].iloc[:, 0].tolist()

xli_tickers =  pd.read_csv(r'../extractors/XLI.csv')[pd.read_csv(r'../extractors/XLI.csv').iloc[:, 0] != "Symbol"].iloc[:, 0].tolist()

xle_tickers =  pd.read_csv(r'../extractors/XLE.csv')[pd.read_csv(r'../extractors/XLE.csv').iloc[:, 0] != "Symbol"].iloc[:, 0].tolist()

xlb_tickers =  pd.read_csv(r'../extractors/XLB.csv')[pd.read_csv(r'../extractors/XLB.csv').iloc[:, 0] != "Symbol"].iloc[:, 0].tolist()


indexes = {
    "S&P 500": tickers,
    "XLP": xlp_tickers,
    "XLU": xlu_tickers,
    "XLK": xlk_tickers,
    "XLY": xly_tickers,
    "XLV": xlv_tickers,
    "XLC": xlc_tickers,
    "XLRE": xlre_tickers,
    "XLF": xlf_tickers,
    "XLI": xli_tickers,
    "XLE": xle_tickers,
    "XLB": xlb_tickers,
}


with open('tickers.json', 'w') as file:
    json.dump(indexes, file)



print(len(xlp_tickers))
print(len(xlu_tickers))
print(len(xlk_tickers))
print(len(xly_tickers))
print(len(xlv_tickers))
print(len(xlc_tickers))
print(len(xlre_tickers))
print(len(xlf_tickers))
print(len(xli_tickers))
print(len(xle_tickers))
print(len(xlb_tickers))