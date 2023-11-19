import pandas as pd
import yfinance as yf
import numpy as np
import winsound
duration = 1000  # milliseconds
freq = 440  # Hz
frame = pd.read_csv('C:/Users/accam/Documents/ms728/Projeto/main/BR/Everything/tickers_data_br_2018-01-01_to_2023-10-05.csv')

import datetime
current_date = datetime.date.today()
print(current_date, '\n')
#%%pegar dados historicos

tickers_data = []
tickers_hist=[]

i = 0
for ticker_symbol in frame['Symbol']:
    try:
        info = yf.download(f'{ticker_symbol}.SA',)
 
        current_price = info['Adj Close'][-1]
        
        index = frame.loc[frame['Symbol'] == ticker_symbol].index[0]
        sector = frame['Sector'][index]
        
        historical_data = info['Adj Close']
        monthly_data = historical_data.resample('M').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'})
        closed_data= np.array(monthly_data['Close'])
        closed_data = closed_data.reshape(closed_data.shape[0],1)     
        tickers_data.append({'Symbol': ticker_symbol, 'Sector': sector, 'Current Price': current_price})
        tickers_hist.append(closed_data)
        i+=1
        
    except:
        i+=1
        
df = pd.DataFrame(tickers_data)

frame_symbol=np.array(df['Symbol'])

desired_size = max(len(arr) for arr in tickers_hist)

index = 0
for array in tickers_hist:
    if len(array)<desired_size:
        nan_array = np.array([np.nan for i in range(desired_size - len(array))]).reshape(desired_size - len(array),1)
        filled_array = np.concatenate((nan_array, array))
        tickers_hist[index]=filled_array
    index+=1

tickers_hist_array=np.array(tickers_hist)
tickers_hist_array=tickers_hist_array.transpose(1, 0, 2)
tickers_hist_array = tickers_hist_array.reshape(tickers_hist_array.shape[0],tickers_hist_array.shape[1])

frame_sectors=np.array(df['Sector'])

frame_prices = np.array(df['Current Price'])

tickers_data= {'Symbol': frame_symbol, 'Sector': frame_sectors, 'Current Price': frame_prices}
df=pd.DataFrame(tickers_data)

df.to_csv(f'data/tickers_data_br_{current_date}.csv', index=False)
np.save(f'data/tickers_historical_array_br_{current_date}.npy', tickers_hist_array)

winsound.Beep(freq, duration)
