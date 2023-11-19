import pandas as pd
import numpy as np

file_date = '2023-11-09'

dados = f'C:/Users/accam/Documents/ms728/Projeto/main/BR/Main/main_files/data/tickers_data_br_{file_date}_preprocess.csv'
historico = f'C:/Users/accam/Documents/ms728/Projeto/main/BR/Main/main_files/data/tickers_historical_array_br_{file_date}_preprocess.npy'
df = pd.read_csv(dados) # dataframe com informacao dos ativos
tickers_hist = np.load(historico) # matriz com precos historicos dos ativos

#%%vetores anteriores

number_vars = len(df['Symbol'])
meus_ativos = ['RNEW4']
quantidades= [38]

investimento_total_anterior = np.array([42.94])
vetor_valor_anterior=np.zeros(number_vars).reshape(number_vars,1) #qntd de cada acao anteriormente

indices = [ ]
for ativo in meus_ativos:
    index = np.where(df['Symbol'] == ativo)[0]
    indices.append(index)

i=0
for indice in indices:
    if len(indice)!= 0:
        vetor_valor_anterior[indice[0]] = quantidades[i]
        i+=1

np.save('C:/Users/accam/Documents/ms728/Projeto/main/BR/Main/main_files/data/investimento_total_anterior.npy', investimento_total_anterior)
np.save('C:/Users/accam/Documents/ms728/Projeto/main/BR/Main/main_files/data/vetor_valor_anterior.npy', vetor_valor_anterior)
