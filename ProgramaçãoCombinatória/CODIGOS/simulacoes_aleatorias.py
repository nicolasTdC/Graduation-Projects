
import modelagem as mc
import numpy as np
import pandas as pd
import random

tempo_investido= 12 #meses

investimento = 10000

investimento=np.array(investimento).reshape(1,1)

frame = pd.read_csv('tickers_data.csv') #dataframe com informacao dos ativos
historical = np.load('tickers_historical_array.npy') #matriz com precos historicos dos ativos

sectors = frame['Sector'].unique()

taxa_livre=0.05 #anual

carteiras=[]
volatilidades=[]
sharpes= []
gastos=[]
retornos_esperados=[]
retornos_proporcao=[]
proporcoes_setor=[]
proporcoes_ativo=[]
proporcoes_carteiras = []

numero_simulacoes=1000

import warnings
warnings.filterwarnings("ignore", message="Spaces are not permitted in the name.*")

investimento_total_anterior =np.zeros(1)
vetor_valor_anterior=np.zeros(frame.shape[0]).reshape(frame.shape[0],1) #qntd de cada acao anteriormente

for i in range(numero_simulacoes):

    proporcao_limite_por_ativo = [random.random() for _ in range(frame.shape[0])]

    proporcao_limite_por_setor = [random.random() for _ in range(len(sectors))]
       
    otimizacao = mc.portifolio(investimento, proporcao_limite_por_ativo, proporcao_limite_por_setor,frame, historical,tempo_investido,taxa_livre, investimento_total_anterior,vetor_valor_anterior)
    
    proporcoes_carteiras.append(otimizacao[9])
    carteiras.append(otimizacao[0])
    gastos.append(otimizacao[2])
    retornos_esperados.append( otimizacao[1])

    volatilidade_portifolio, indice_sharpe, retorno=round(otimizacao[3][0],2),round(otimizacao[4][0][0],2),round(otimizacao[5][0][0],2)
    
    volatilidades.append(volatilidade_portifolio)
    sharpes.append(indice_sharpe)
    retornos_proporcao.append(retorno)
    
    proporcoes_setor.append(proporcao_limite_por_setor)
    proporcoes_ativo.append(proporcao_limite_por_ativo)
    
#%%
import matplotlib.pyplot as plt

maior_sharpe=max(sharpes)

indice_maior_sharpe= np.where(sharpes == maior_sharpe)[0][0]

plt.scatter(volatilidades,retornos_proporcao)

highlight_x = volatilidades[indice_maior_sharpe]
highlight_y = retornos_proporcao[indice_maior_sharpe]
plt.scatter(highlight_x, highlight_y, color='red', label='Maior Sharpe')

plt.xlabel('Volatilidade')
plt.ylabel('Retorno')
plt.legend()

plt.show()

#%%
melhor_carteira = carteiras[indice_maior_sharpe]
coluna2=[]
coluna1=[]
for key in  melhor_carteira:
    coluna1.append(key)
    coluna2.append(melhor_carteira[key])

sectors_indexes = {}
for ticker in coluna1:
    index = np.where(frame['Symbol'] == ticker)[0][0]
    sectors_indexes[ticker] =  index

indexes_setores=list(sectors_indexes.values())
setores_ativos=[frame['Sector'][i] for i in indexes_setores ]

proporcao_carteira_ativos_nao_zero =[x for x in proporcoes_carteiras[indice_maior_sharpe] if x != 0] 


data = {
    'Sigla': coluna1,
    'Setor':setores_ativos,
    'Quantidade': coluna2,
    'Proporcao': proporcao_carteira_ativos_nao_zero
}

df=pd.DataFrame(data)
sorted_df = df.sort_values(by='Setor')

print('Para melhor carteira:')
print(sorted_df.to_string(index=False))
print('Retorno esperado = $', round(retornos_esperados[indice_maior_sharpe][0][0], 2))
print('Dinheiro gasto = $', round(gastos[indice_maior_sharpe][0][0],2))
print('Ganho de $', round(retornos_esperados[indice_maior_sharpe][0][0]-gastos[indice_maior_sharpe][0][0], 2))

print(f'Retorno = {retornos_proporcao[indice_maior_sharpe]} , Volatilidade={volatilidades[indice_maior_sharpe]} , Indice Sharpe = {maior_sharpe}')
#%%
np.save('proporcoes_aleat_ativos.npy', proporcoes_ativo[indice_maior_sharpe])
np.save('proporcoes_aleat_setor.npy', proporcoes_setor[indice_maior_sharpe])
