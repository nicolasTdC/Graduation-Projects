
import modelagem as mc
import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings("ignore", message="Spaces are not permitted in the name.*")

print('Otimização de carteira')
print()
print('---------------------------------------------------------------------------------')
print()
print('I) Dados considerados:')
print()

frame = pd.read_csv(input('Extrair dados dos ativos de que arquivo? ')) #tickers_data.csv
#dataframe com informacao dos ativos
 
historical = np.load(input('Precos historicos de que arquivo? ')) #tickers_historical_array.npy 
#matriz com precos historicos dos ativos

decisao1= input('Considerar ações específicas? (S / N) ') 
if decisao1 == 'S':
    numero_arbitrario = int(input('Quantas ações serão consideradas? '))
    siglas_consideradas = [input(f'Digite a sigla da ação {_+1}: ') for _ in range(numero_arbitrario)]
    index_siglas_consideradas =[]
    for _ in siglas_consideradas:
        index_siglas_consideradas.append(np.where(frame['Symbol'] == _)[0][0])
        
    frame = frame.iloc[index_siglas_consideradas].reset_index(drop=True)
    historical = historical[:, index_siglas_consideradas]

else:
    siglas_consideradas = frame['Symbol']
    
#%%
print()
print('---------------------------------------------------------------------------------')
print()
print('II) Variáveis da carteira:')
print()

tempo_investido=float(input('Tempo investido em meses: ')) #12 #meses

investimento = float(input('Dinheiro investido: ')) #10000
investimento = np.array(investimento).reshape(1,1)

taxa_livre=float(input('Taxa anual livre de risco: ( exemplo: se 5%, digite 0.05 ) '))#0.05 #anual

sectors = frame['Sector'].unique()

decisao2 = input('Limites para gasto proporcianais dos ativos IGUAIS ou DIFERENTES? (I / D): ')    #limite de recurso alocado para cada ativo 


if decisao2 == 'D':
    
    proporcao_limite_por_ativo =np.array([ float(input(f'Proporcao limite para gasto para {_}: ')) for _ in siglas_consideradas ])
    
else:
    prop_arbitraria = float(input('Proporcao de gasto igual para ativos: '))
    proporcao_limite_por_ativo =np.array([ prop_arbitraria for _ in range(frame.shape[0]) ])


decisao3 = input('Limites de gasto proporcianais dos setores IGUAIS ou DIFERENTES? (I / D): ')    #limite de recurso alocado para cada ativo 


if decisao3 == 'D':
    
    proporcao_limite_por_setor =np.array([ float(input(f'Proporcao limite de gasto para setor{_+1}: ')) for _ in range(len(sectors)) ])
    
else:
    prop_arbitraria = float(input('Proporcao de gasto igual para setores: '))
    proporcao_limite_por_setor =np.array([ prop_arbitraria for _ in range(len(sectors)) ])


decisao4 = input('Otimizar carteira anterior ou obter carteira nova? (ANTERIOR / NOVA): ')


if decisao4 == 'NOVA':

    investimento_total_anterior =np.zeros(1)
    vetor_valor_anterior=np.zeros(frame.shape[0]).reshape(frame.shape[0],1) #qntd de cada acao anteriormente

else: 
    investimento_total_anterior= np.array(float(input('Quantidade de investimento anterior: '))).reshape(1,1)
    decisao5 = input('Digitar quantidade de cada açao separadamente ou o vetor?: (SEPARADO / VETOR) ')
    if decisao5 == 'SEPARADO':
            
        vetor_valor_anterior = np.array([ float(input(f'Quantidade possuida de {_}: ')) for _ in siglas_consideradas ])
    else:
       # vetor_valor_anterior = np.array((input('Vetor possuida de cada ação : ')).split())
        vetor_valor_anterior =(input('Elementos do vetor da quantidade possuida de cada ação : ( exemplo: 12 33 50 etc )')).split()
        vetor_valor_anterior_float = [float(x) for x in vetor_valor_anterior]
        vetor_valor_anterior=np.array(vetor_valor_anterior_float).reshape(frame.shape[0],1)

print()
print('---------------------------------------------------------------------------------')
print()
print('III) Portifolio recomendado: ')
print()
#%%
otimizacao = mc.portifolio(investimento, proporcao_limite_por_ativo, proporcao_limite_por_setor,frame, historical,tempo_investido,taxa_livre, investimento_total_anterior,vetor_valor_anterior)

if otimizacao != 0:
        
    portifolio = otimizacao[0]
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
        
    sectors_indexes = {}
    for ticker in coluna1:
        index = np.where(frame['Symbol'] == ticker)[0][0]
        sectors_indexes[ticker] =  index
    
    indexes_setores=list(sectors_indexes.values())
    setores_ativos=[frame['Sector'][i] for i in indexes_setores ]
    
    #proporcao_total_da_iteracao=sum(coluna2)
    #proporcao_carteira_ativos_nao_zero = [ i *  / investimento for  i in coluna2]
    proporcao_carteira_ativos_nao_zero =[x for x in proporcao_carteira_iteracao if x != 0] 
    
    
    
    data = {
        'Sigla': coluna1,
        'Setor':setores_ativos,
        'Quantidade': coluna2,
        'Proporcao': proporcao_carteira_ativos_nao_zero
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
    
    print(f'Retorno = {retorno} , Volatilidade={volatilidade_portifolio} , Indice Sharpe = {indice_sharpe}')
    #%%
    if decisao4 == 'ANTERIOR':
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
            'Proporcao na carteira': proporcao_carteira_nonzero
        }
        
        df=pd.DataFrame(data)
        sorted_df = df.sort_values(by='Setor')
        print(sorted_df.to_string(index=False))
        
    
#%%
