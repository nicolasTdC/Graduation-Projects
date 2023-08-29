# -*- coding: utf-8 -*-
"""
Created on Fri May 19 11:19:17 2023

@author: Nick
"""

import pandas as pd
import yfinance as yf
import numpy as np

# Obtém a lista de símbolos de ações disponíveis
tickers = pd.read_csv('https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv')
#%%
# Cria um objeto Ticker para cada ação e obtém informações adicionais
tickers_data = []
tickers_hist=[]

i = 0
for ticker_symbol in tickers['Symbol']:

    ticker = yf.Ticker(ticker_symbol)
    
    current_price = ticker.info.get('regularMarketPreviousClose')
    
    if current_price is None:
        i+=1
        continue
    
    sector = tickers['GICS Sector'][i]
    
    historical_data = ticker.history(period='1d', start='2018-01-01', end='2023-05-01')
    monthly_data = historical_data.resample('M').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'})
    closed_data= np.array(monthly_data['Close'])
    
    
    tickers_data.append({'Symbol': ticker_symbol, 'Sector': sector, 'Current Price': current_price})
    tickers_hist.append(closed_data)

    i+=1

# Cria um DataFrame com os dados dos ativos
df = pd.DataFrame(tickers_data)

#%%exportar dados

df.to_csv('tickers_data.csv', index=False)

tickers_hist_array=np.array(tickers_hist)
hist_array=np.zeros(64*501).reshape(64,501)

i=0
for v in tickers_hist_array:
    #v.reshape(1,len(v))
    if len(v)<64:
        v0 = np.zeros(64)
        v0[(64-len(v)):]= v
        v=v0
        
    hist_array[:,i] = v
    i+=1

np.save('tickers_historical_array.npy', hist_array)

