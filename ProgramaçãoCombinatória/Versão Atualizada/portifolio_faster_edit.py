
import modelagem_br as mc
import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings("ignore", message="Spaces are not permitted in the name.*")

file_date = '2023-11-09'

frame = pd.read_csv(f'C:/Users/accam/Documents/ms728/Projeto/main/BR/Main/main_files/data/tickers_data_br_{file_date}_preprocess.csv')
historical = np.load(f'C:/Users/accam/Documents/ms728/Projeto/main/BR/Main/main_files/data/tickers_historical_array_br_{file_date}_preprocess.npy')

t = tempo_investido = 1#meses

taxa_livre=0.1225 #anual

investimento =  350.68 + 66.34

prop_arbitraria_ativo = 1/3 * 1/2

prop_arbitraria_setor = 1/3

CARTEIRA_ANTERIOR = 1 #-1 SE CARTEIRA NOVA

INVETIMENTO_ANTERIOR = 0

siglas_consideradas = frame['Symbol']
    
investimento = np.array(investimento).reshape(1,1)

sectors = frame['Sector'].unique()

proporcao_limite_por_ativo =np.array([ prop_arbitraria_ativo for _ in range(frame.shape[0]) ])

proporcao_limite_por_setor =np.array([ prop_arbitraria_setor for _ in range(len(sectors)) ])

if CARTEIRA_ANTERIOR == -1:
    investimento_total_anterior =np.zeros(1)
    vetor_valor_anterior=np.zeros(frame.shape[0]).reshape(frame.shape[0],1) #qntd de cada acao anteriormente
else:
    investimento_total_anterior = np.load('C:/Users/accam/Documents/ms728/Projeto/main/BR/Main/main_files/data/investimento_total_anterior.npy')
    vetor_valor_anterior= np.load('C:/Users/accam/Documents/ms728/Projeto/main/BR/Main/main_files/data/vetor_valor_anterior.npy')


otimizacao = mc.portifolio(investimento, proporcao_limite_por_ativo,
                           proporcao_limite_por_setor, frame,
                           historical,tempo_investido,taxa_livre,
                           investimento_total_anterior,vetor_valor_anterior)

if otimizacao != 0:
        
    portifolio = otimizacao[0]
    gasto=otimizacao[2]
    funcao_objetivo = otimizacao[1]
    volatilidade_portifolio, indice_sharpe, retorno=round(otimizacao[3][0],2),round(otimizacao[4][0][0],2),round(otimizacao[5][0][0],2)
    vetor_valor_acumulado= otimizacao[6]
    investimento_total_acumulado = otimizacao[7]
    proporcao_carteira = otimizacao[8]#acumulado
    proporcao_carteira_iteracao = otimizacao[9]
    target_prices = otimizacao[-1]

    coluna2=[]
    coluna1=[]
    target_prices_active = []

    for key in  portifolio:
        coluna1.append(key)
        coluna2.append(portifolio[key])
    preco_considerado=[]    
    sectors_indexes = {}
    for ticker in coluna1:
        index = np.where(frame['Symbol'] == ticker)[0][0]
        sectors_indexes[ticker] =  index
        preco_considerado.append(frame['Current Price'][index])
        target_prices_active.append(target_prices[index][0])
        
    
    indexes_setores=list(sectors_indexes.values())
    setores_ativos=[frame['Sector'][i] for i in indexes_setores ]
 
    proporcao_carteira_ativos_nao_zero =[x for x in proporcao_carteira_iteracao if x != 0] 
    
    data = {
        'Sigla': coluna1,
        'Setor':setores_ativos,
        'Quantidade': coluna2,
        'Proporcao': proporcao_carteira_ativos_nao_zero,
        'Preco considerado por unidade':  preco_considerado,
        'Preco alvo':  target_prices_active
    }
    
    df=pd.DataFrame(data)
    sorted_df = df.sort_values(by='Setor')
 
    print()
    print('Carteira da iteração: ')
    print()
    
    print(sorted_df.to_string(index=False))
    print('Retorno esperado = $', round(funcao_objetivo[0][0], 2))
    print('Dinheiro gasto = $', round(gasto[0][0],2))
    print('Ganho de $', round(funcao_objetivo[0][0]-gasto[0][0], 2))
    print('Ivista em renda fixa: $', round(investimento - gasto[0][0], 2))

    print(f'Retorno = {retorno} , Volatilidade={volatilidade_portifolio} , Indice Sharpe = {indice_sharpe}')
    
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
        'Quantidade':quantidade_acumulada ,
        'Proporcao na carteira': proporcao_carteira_nonzero,
        
    }
    
    df=pd.DataFrame(data)
    sorted_df = df.sort_values(by='Setor')
    print(sorted_df.to_string(index=False))
        
import winsound
duration = 1000  # milliseconds
freq = 440  # Hz
winsound.Beep(freq, duration)


