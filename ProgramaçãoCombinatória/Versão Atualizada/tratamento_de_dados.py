import pandas as pd
import numpy as np

file_date = '2023-11-09'

dados = f'C:/Users/accam/Documents/ms728/Projeto/main/BR/Main/main_files/data/tickers_data_br_{file_date}.csv'
historico = f'C:/Users/accam/Documents/ms728/Projeto/main/BR/Main/main_files/data/tickers_historical_array_br_{file_date}.npy'
df = pd.read_csv(dados) # dataframe com informacao dos ativos
tickers_hist = np.load(historico) # matriz com precos historicos dos ativos

frame_symbol=np.array(df['Symbol'])
frame_prices = np.array(df['Current Price'])
frame_sectors=np.array(df['Sector'])

#%%
#retirar os desvio padrao zero
std_deviations = np.std(tickers_hist, axis=0)
zero_std_indices = np.where(std_deviations == 0)[0]
tirar=zero_std_indices

frame_symbol = np.delete(frame_symbol, tirar)

frame_prices = np.delete(frame_prices, tirar)

frame_sectors = np.delete(frame_sectors, tirar)

tickers_hist = np.delete(tickers_hist, tirar,axis=1)     

#%%
#Remover um index especifico
flag_tirar = 1 #-1 pra n tirar nada

lista_tirar = np.array(['QUAL3', 'PLRI11', 'XPCM11', 'DISB34', 'TRVC34', 'RECT11', 'RDNI3', 'RCSL4', 
                        'XRXB34', 'RBDS11', 'BRPR3', 'VAMO3', 'OIBR4', 'SLED3', 'AHEB3', 'CEOC11'])

if flag_tirar != -1:
    
    for _ in lista_tirar:
        
        tirar = np.where(frame_symbol == _)
        
        frame_symbol = np.delete(frame_symbol, tirar)
        
        frame_prices = np.delete(frame_prices, tirar)
        
        frame_sectors = np.delete(frame_sectors, tirar)
        
        tickers_hist = np.delete(tickers_hist, tirar,axis=1)     

#%%
#salvar
tickers_data= {'Symbol': frame_symbol, 'Sector': frame_sectors, 'Current Price': frame_prices}

df=pd.DataFrame(tickers_data)

df.to_csv(f'C:/Users/accam/Documents/ms728/Projeto/main/BR/Main/main_files/data/tickers_data_br_{file_date}_preprocess.csv', index=False)

np.save(f'C:/Users/accam/Documents/ms728/Projeto/main/BR/Main/main_files/data/tickers_historical_array_br_{file_date}_preprocess.npy', tickers_hist)
