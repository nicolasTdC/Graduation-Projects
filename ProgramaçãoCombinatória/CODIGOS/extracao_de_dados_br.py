import pandas as pd
import yfinance as yf
import numpy as np
import investpy as inv

# Obtém a lista de símbolos de ações disponíveis
#%%
tickers=inv.stocks.get_stocks(country='brazil')

#%%
# Cria um objeto Ticker para cada ação e obtém informações adicionais
tickers_data = []
tickers_hist=[]

i = 0
for ticker_symbol in tickers['symbol']:

    ticker = yf.Ticker(f'{ticker_symbol}.SA')
    
    try:
        current_price = ticker.info.get('regularMarketPreviousClose')
        
        if current_price is None:
            i+=1
            continue
        
        #sector = tickers['GICS Sector'][i]
        sector = ticker.info.get('sector', 'N/A')
        
        historical_data = ticker.history(period='1d', start='2022-01-01', end='2023-06-15')
        monthly_data = historical_data.resample('M').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'})
        closed_data= np.array(monthly_data['Close'])
    
    
        tickers_data.append({'Symbol': ticker_symbol, 'Sector': sector, 'Current Price': current_price})
        tickers_hist.append(closed_data)
        i+=1
    except:
        i+=1

# Cria um DataFrame com os dados dos ativos
df = pd.DataFrame(tickers_data)

#%%exportar dados

df.to_csv('tickers_data_br.csv', index=False)

tickers_hist_array=np.array(tickers_hist)
hist_array=np.zeros(len(tickers_hist_array[0])*len(tickers_data)).reshape(len(tickers_hist_array[0]),len(tickers_data))

i=0
for v in tickers_hist_array:
    #v.reshape(1,len(v))
    if len(v)<len(tickers_hist_array[0]):
        v0 = np.zeros(len(tickers_hist_array[0]))
        v0[(len(tickers_hist_array[0])-len(v)):]= v
        v=v0
        
    hist_array[:,i] = v
    i+=1

np.save('tickers_historical_array_br.npy', hist_array)

