# -*- coding: utf-8 -*-
import warnings
import numpy as np
import pulp
from pulp import LpProblem, LpVariable, LpInteger, LpMaximize#, LpStatus
warnings.filterwarnings("ignore", category=RuntimeWarning,
                        message="divide by zero encountered in divide")
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

#%%indice_sharpe_obj do preco em t meses

def previsao_preco(t, historical_price,current_price,taxa_livre):
        
    valid_prices =  historical_price
    
    primeiro_valor = valid_prices[0]
    
    _ = 1
    while _ < len(valid_prices) and valid_prices[_] == primeiro_valor:
        _ += 1
    
    remore_till = _ 
    
    valid_prices = valid_prices[remore_till+1:]
    
    valid_prices = valid_prices[~np.isnan(valid_prices)]

    std = np.std(valid_prices)
    
    train_data = valid_prices
    dataset_train = train_data.reshape(valid_prices.shape[0],1)
    
    scaler = MinMaxScaler(feature_range = (0,1))
    dataset_train_scaled = scaler.fit_transform(dataset_train)

    X_train = []
    y_train = []
     
    time_step = 50
    
    length_validation = length_train = valid_prices.shape[0]
    while time_step >= length_validation:
        time_step = round(time_step/2)
        
    for i in range(time_step, length_train):
         X_train.append(dataset_train_scaled[i-time_step:i,0])
         y_train.append(dataset_train_scaled[i,0])

    # convert list to array
    X_train, y_train = np.array(X_train), np.array(y_train)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1],1))
    y_train = np.reshape(y_train, (y_train.shape[0],1))

      
    model_lstm = Sequential()
    model_lstm.add(LSTM(64, return_sequences=True,input_shape = (X_train.shape[1], 1))) #64 lstm neuron block
    model_lstm.add(LSTM(64, return_sequences= False))
    model_lstm.add(Dense(32))
    model_lstm.add(Dense(1))
    model_lstm.compile(loss = "mean_squared_error", optimizer = "adam", metrics = ["accuracy"])
    
    X_input = valid_prices[-time_step:]
    
    X_input = scaler.fit_transform(X_input.reshape(-1,1))      # converting to 2D array and scaling
    X_input = np.reshape(X_input, (1,time_step,1))
    
    LSTM_prediction = scaler.inverse_transform(model_lstm.predict(X_input, verbose=0))
    
    y_pred = LSTM_prediction[0,0]
    
    sharpe = (y_pred - (1+taxa_livre*t/12)*current_price)/std 
    
    if y_pred < current_price:
        return np.array(float(-9999999)).reshape(1,1), y_pred
    
    return np.array(sharpe) ,y_pred

#%%vetor b

def criar_b(recurso_total, vetor_limite,sector_num): # vetor_limite = vetor com proporcao limite de cada setor
        
    vetor_limite=np.array(vetor_limite).reshape(sector_num,1)
    b = np.zeros([1 + sector_num ,1])
    b[0]=recurso_total
    b[1:]=vetor_limite*recurso_total
    return b

#%%
def matriz_correlacao(X,m,n):
    mean=[]#media para cada atributo
    std=[]#std para cada atributo
    for i in range(n):
        mi = np.mean(X[:,i])
        sigma=np.std(X[:,i])
        mean.append(mi)
        std.append(sigma)
    for j in range(n):
        for i in range(m):
            if std[j]!=0:
                X[i,j]=(X[i,j]-mean[j])/std[j]#z score dos atributos]
            else:
                X[i,j]=(X[i,j]-mean[j])
            
    Sigma=1/m*X.T@X#matriz cor
    
    return mean,std,Sigma

#%%funcao principal

def portifolio(investimento, proporcao_limite_por_ativo, proporcao_limite_por_setor,
               frame, historical,tempo_investido,taxa_livre, investimento_total_anterior, vetor_valor_anterior):
    
    
    frame_symbol=np.array(frame['Symbol'])

    element_list=[]
    indexes_repetidos=[]
    for element in frame_symbol:
        if element not in element_list:
            element_list.append(element)
        else:
            index_repetido = np.where(frame_symbol==element)[0]
            indexes_repetidos.append(index_repetido)
    
    duplicated_indexes = []
    for lista in indexes_repetidos:
        for numero_elementos in range(len(lista)-1):
            duplicated_indexes.append(lista[numero_elementos+1])

    frame_symbol = np.delete(frame_symbol, duplicated_indexes)
    
    vetor_valor_anterior = np.delete(vetor_valor_anterior, duplicated_indexes)


    frame_prices = np.array(frame['Current Price'])
    frame_prices = np.delete(frame_prices, duplicated_indexes)

    frame_sectors=np.array(frame['Sector'])
    frame_sectors = np.delete(frame_sectors, duplicated_indexes)
    
    historical = np.delete(historical, duplicated_indexes, axis=1)
    
    nan_columns = np.where(np.isnan(historical).any(axis=0))[0]
    
    for column_index in nan_columns:
        nan_indices = np.isnan(historical[:, column_index])
    
        # Calculate the mean of the non-NaN elements in the column
        column_mean = np.nanmean(historical[:, column_index])
        
        # Replace NaN elements with the column mean
        historical[nan_indices, column_index] = column_mean
    
    indice_sharpe_obj=[]
    previsao_not_norm=[]
    for i in range(historical.shape[1]):
       # if frame['Symbol'][i] == 'PINE4':
         #   print(1)
        prev = previsao_preco(tempo_investido, historical[:,i],frame_prices[i],taxa_livre)
        
        previsao_not_norm.append(prev[1])
        
        if (previsao_not_norm[i]<frame_prices[i]) or (prev[0]<0) :
            indice_sharpe_obj.append(np.array([[float(-9999999)]])) 
        else:
            indice_sharpe_obj.append(prev[0]) 

    frame_sector_string =[str(sec) for sec in  frame_sectors]
    sectors = np.unique(frame_sector_string)
    sector_num=sectors.shape[0]
    sectors_indexes = {}
    frame_sector_string =[str(sec) for sec in  frame_sectors]
    for sector in sectors:
        sector_str = str(sector)
        sector_index = f"{sector}_index"
    
        sector_list = [i for i, sec in enumerate(frame_sector_string) if sec == sector_str]
        sectors_indexes[sector_index] = sector_list

    # cria matria de coefientes de restricoes A

    A_num_colunas=historical.shape[1]
        # numero vars de decisao
    A_num_linhas = 1 + sectors.shape[0]
        # restricao recurso total = 1
        # restricao recurso para cada setor = numero setores
        
    A0 = np.zeros([A_num_linhas,A_num_colunas])

    A0[0,:]= frame_prices # coefientes para restricao de recursos total

    i = 1
    ordem_setores=[]
    for sector in sectors_indexes:
        ordem_setores.append(sector)
        for index in sectors_indexes[sector]:
            A0[i,index] = frame_prices[index] # coefientes para restricao de cada setor
        i+=1

    b= criar_b(investimento, proporcao_limite_por_setor,sector_num)
        # cria vetor b

    # Cria problema de maximizacao
    problem = LpProblem("Large LP", LpMaximize)
    
    # Define numero vars e restricoes
    num_variables = A0.shape[1]
    num_constraints = A0.shape[0]

    # Cria variaveis
    ativos =frame_symbol
    variables = [LpVariable(f'{ativos[i]}', lowBound=0,upBound=(proporcao_limite_por_ativo[i]*investimento/A0[0][i]), cat=LpInteger) for i in range(num_variables)]

    # Define funcao objetivo
    if investimento_total_anterior[0] != 0:
        
        proporcao_carteira_anterior=[]
        
        for i in range(num_variables):
            vetor_valor_anterior = vetor_valor_anterior.reshape(A_num_colunas,1)
            proporcao_carteira_anterior.append(((A0[0][i]* vetor_valor_anterior[i] ) /investimento_total_anterior )[0])
        
    
    else:
        vetor_valor_anterior=np.zeros(A_num_colunas)
        proporcao_carteira_anterior=np.zeros(A_num_colunas)
        
    objective_coeffs = [indice_sharpe_obj[i]*np.exp(-proporcao_carteira_anterior[i]) for i in range(num_variables)]

    problem += sum(variables[i] * objective_coeffs[i] for i in range(num_variables)) #adiciona funcao obj ao problema

    # Adiciona restricoes
    for j in range(num_constraints):
        constraint_coeffs = [A0[j][i] for i in range(num_variables)]
        constraint = sum(variables[i] * constraint_coeffs[i] for i in range(num_variables)) <= b[j]
        problem += constraint
    
    solver1 = pulp.PULP_CBC_CMD(msg=False)

    try:
        problem.solve(solver1)
    except:
        print('Não vale a pena comprar nenhuma ação.')
        return 0

    var_value=[]
    for variable in variables:
        var_value.append((f"{variable.name} = {variable.value()}"))

    value_dic = {s.split(' = ')[0]: float(s.split(' = ')[1]) for s in var_value}

    vetor_valor=np.array([ value_dic[key] for key in value_dic ]).reshape(num_variables,1)

    retorno_esperado = np.transpose(np.array(previsao_not_norm).reshape(num_variables,1))@vetor_valor #retorno bruto
    
    portifolio_dic={}
    for key in value_dic:
        if value_dic[key] != 0:
            portifolio_dic[key] = value_dic[key]
            
    gasto =  np.transpose(frame_prices.reshape(num_variables,1))@vetor_valor
    
    matriz_cor= matriz_correlacao(historical,historical.shape[0],historical.shape[1])[2]

    peso_total=sum(vetor_valor)
    
    if peso_total == 0:
        print('Não vale a pena comprar nenhuma ação.')
        return 0
    
    vetor_peso_ativos=[i[0]/peso_total[0] for i in vetor_valor]
    
    
    vetor_valor_acumulado = vetor_valor_anterior+vetor_valor
    investimento_total_acumulado = investimento_total_anterior+ investimento
    proporcao_carteira_atualizado=[]
    proporcao_carteira_iteracao=[]
    for i in range(num_variables):
        
        proporcao_carteira_atualizado.append(((A0[0,i] *  vetor_valor_acumulado[i])/investimento_total_acumulado )[0][0])
    
   
        proporcao_carteira_iteracao.append(((A0[0,i] *  vetor_valor[i])/investimento )[0][0])


    variacao_portifolio = np.transpose(np. array(vetor_peso_ativos).reshape(num_variables,1)) @ matriz_cor @ np.array(vetor_peso_ativos)

    volatilidade_portifolio = np.sqrt(variacao_portifolio)
    
    retorno= retorno_esperado/gasto-1 #fracao em relacao ao gasto
    
    indice_sharpe=retorno/volatilidade_portifolio
    

    return portifolio_dic, retorno_esperado, gasto, volatilidade_portifolio, indice_sharpe,retorno,vetor_valor_acumulado,investimento_total_acumulado,proporcao_carteira_atualizado,proporcao_carteira_iteracao, np.array(previsao_not_norm).reshape(num_variables,1)
