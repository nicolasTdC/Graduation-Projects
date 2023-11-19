import modelagem_br as mc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore", message="Spaces are not permitted in the name.*")
warnings.filterwarnings("ignore", category=UserWarning,
                        message="A NumPy version >=1.16.5 and <1.23.0 is required for this version of SciPy ")

file_date = '2023-11-09'

frame = pd.read_csv(f'C:/Users/accam/Documents/ms728/Projeto/main/BR/Main/main_files/data/tickers_data_br_{file_date}_preprocess.csv')
historical = np.load(f'C:/Users/accam/Documents/ms728/Projeto/main/BR/Main/main_files/data/tickers_historical_array_br_{file_date}_preprocess.npy')

'''
frame = frame.head(40)
historical = historical[:,:40]
'''

taxa_livre = 0.1225

t = tempo_investido = 1 # 1 mes padrao

tempo_treino = historical.shape[0]-t
historical_teste = historical[:tempo_treino,:]

for i in range(len(frame['Current Price'])):
    frame.loc[i, 'Current Price'] = historical[-t-1,i]

investimento =  350.68 + 66.34

prop_arbitraria_ativo = 1/3 * 1/2

prop_arbitraria_setor = 1/3

siglas_consideradas = frame['Symbol']
    
investimento = np.array(investimento).reshape(1,1)

sectors = frame['Sector'].unique()

proporcao_limite_por_ativo =np.array([ prop_arbitraria_ativo for _ in range(frame.shape[0]) ])

proporcao_limite_por_setor =np.array([ prop_arbitraria_setor for _ in range(len(sectors)) ])

investimento_total_anterior = np.load('C:/Users/accam/Documents/ms728/Projeto/main/BR/Main/main_files/data/investimento_total_anterior.npy')

vetor_valor_anterior= np.load('C:/Users/accam/Documents/ms728/Projeto/main/BR/Main/main_files/data/vetor_valor_anterior.npy')

otimizacao = mc.portifolio(investimento, proporcao_limite_por_ativo, proporcao_limite_por_setor,frame,
                           historical_teste,tempo_investido,taxa_livre,
                           investimento_total_anterior,vetor_valor_anterior)

portifolio = otimizacao[0]
target_prices = otimizacao[-1]

#%%        
gasto=otimizacao[2]
funcao_objetivo = otimizacao[1]
volatilidade_portifolio, indice_sharpe, retorno=round(otimizacao[3][0],2),round(otimizacao[4][0][0],2),round(otimizacao[5][0][0],2)
vetor_valor_acumulado= otimizacao[6]
investimento_total_acumulado = otimizacao[7]
proporcao_carteira = otimizacao[8]#acumulado
proporcao_carteira_iteracao = otimizacao[9]

coluna2=[]
coluna1=[]
for key in  portifolio:
     coluna1.append(key)
     coluna2.append(portifolio[key])
preco_considerado=[]    
sectors_indexes = {}
preco_real = []
target_prices_active = []
for ticker in coluna1:
     index = np.where(frame['Symbol'] == ticker)[0][0]
     sectors_indexes[ticker] =  index
     preco_considerado.append(frame['Current Price'][index])
     preco_real.append(historical[-1,index])
     target_prices_active.append(target_prices[index][0])
 
indexes_setores=list(sectors_indexes.values())
setores_ativos=[frame['Sector'][i] for i in indexes_setores ]
 
proporcao_carteira_ativos_nao_zero =[x for x in proporcao_carteira_iteracao if x != 0] 
 
data = {
     'Sigla': coluna1,
     'Setor':setores_ativos,
     'Quantidade': coluna2,
     'Proporcao': np.round(proporcao_carteira_ativos_nao_zero, 2),
     'Preco considerado por unidade':  np.round(preco_considerado, 2),
     'Preco alvo':  np.round( target_prices_active,2 )
 }

df=pd.DataFrame(data)
sorted_df = df.sort_values(by='Setor')
print(sorted_df.to_string(index=False))

gasto_total = np.dot(np.transpose(coluna2) ,preco_considerado) 

preco_real_total = np.dot(np.transpose(coluna2) ,preco_real) 

lucro_real = preco_real_total -  gasto_total
print("Gasto:" , round(gasto_total, 2))
percentual = round((lucro_real/gasto_total - 1) * 100, 2)
print("Lucro real seria:" , round(lucro_real, 2), f'( {percentual} % )')
df=pd.DataFrame(data)
sorted_df = df.sort_values(by='Setor')
 

siglas=[]
for key in portifolio:
    siglas.append(key)

tempo_treino = historical.shape[0]-t
x = np.linspace(0, t-1, t).reshape(-1, 1)
x_future = np.linspace(t, t + t -1, t).reshape(-1, 1)

#x_orig = np.linspace(-(historical.shape[0]-t),-1,(historical.shape[0]-t)).reshape(-1, 1)
x_orig = np.linspace(-6,-1,6).reshape(-1, 1)

for index in range(len(frame)):

    ativo = frame['Symbol'][index]
    if ativo in siglas:
        ativo_index = np.where(frame['Symbol'] == ativo)[0][0]
        historical_price = historical[:tempo_treino,ativo_index]
        historical_price_full = historical[:,ativo_index]
        current_price= frame['Current Price'][ativo_index]
                
        future_data = target_prices[index]

        plt.plot(np.concatenate((x_orig,x)), historical[-7:,ativo_index])
        
        plt.scatter(x, future_data)
        
        x_total = np.concatenate((x_orig,x))
        y_total = np.concatenate((historical[-7:tempo_treino,ativo_index],np.array(future_data).reshape(1,)))
        plt.plot(x_total,y_total, label='Modeled' )
        plt.plot(x_total,historical[-7:,ativo_index], label='Original' )
           
        plt.title(f"{ativo}")
        plt.xlabel('Tempo')
        plt.ylabel('Valor')
        plt.legend()
        plt.show()

print()
print('Carteira acumulada: ')
print()

proporcao_carteira_nonzero = [x for x in proporcao_carteira if x != 0]

nonzero_indices_valor_acumulado = np.nonzero(vetor_valor_acumulado)[0]   

coluna_siglas =[ frame['Symbol'][i] for i in nonzero_indices_valor_acumulado  ]

coluna_setores = [ frame['Sector'][i] for i in nonzero_indices_valor_acumulado  ]

quantidade_acumulada= [ vetor_valor_acumulado[i][0] for i in nonzero_indices_valor_acumulado  ]

data = {
    'Sigla': coluna_siglas,
    'Setor':coluna_setores,
    'Quantidade': quantidade_acumulada ,
    'Proporcao na carteira': np.round( proporcao_carteira_nonzero,2 ),
    
}

df=pd.DataFrame(data)
sorted_df = df.sort_values(by='Setor')
print(sorted_df.to_string(index=False))

#%%
import winsound
duration = 1000  # milliseconds
freq = 440  # Hz
winsound.Beep(freq, duration)
