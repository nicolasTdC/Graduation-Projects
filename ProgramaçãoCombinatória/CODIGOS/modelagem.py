# -*- coding: utf-8 -*-
"""
Created on Fri May 19 18:43:49 2023

@author: Nick
"""

import numpy as np
from sklearn.linear_model import LinearRegression
import pulp
from pulp import LpProblem, LpVariable, LpInteger, LpMaximize, LpStatus

#%%indice_sharpe_obj do preco em t meses

def previsao_preco(t, historical_price,current_price,taxa_livre):
       
    model = LinearRegression()
    
    prices = []
    for p in historical_price:
        
        if np.isnan(p):
            continue
            
        elif (p !=0):
            
            prices.append(p)
    if len(prices) ==0:
        sharpe = 0
        return sharpe
 
    X = np.array(list(range(-(len(prices)-1),1))).reshape(-1,1)
    y =np.array(prices).reshape(-1,1)
    model.fit(X, y)
    new_data = np.array([[t]])
    sharpe = (model.predict(new_data) - (1+taxa_livre*t/12)*current_price)/np.std(prices)

    predicted_not_norm = model.predict(new_data)
    
    return sharpe,predicted_not_norm

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
            X[i,j]=(X[i,j]-mean[j])/std[j]#z score dos atributos]
            
    Sigma=1/m*X.T@X#matriz cor
    
    return mean,std,Sigma

#%%funcao principal

def portifolio(investimento, proporcao_limite_por_ativo, proporcao_limite_por_setor, frame, historical,tempo_investido,taxa_livre, investimento_total_anterior,vetor_valor_anterior):
    
    zero_columns = np.where(np.all(historical == 0, axis=0))[0]

    historical = np.delete(historical, zero_columns, axis=1)
    
    indice_sharpe_obj=[]
    previsao_not_norm=[]
    #%%
    for i in range(historical.shape[1]):
        prev = previsao_preco(tempo_investido, historical[:,i],np.array(frame['Current Price'])[i],taxa_livre)
        indice_sharpe_obj.append(prev[0])
        previsao_not_norm.append(prev[1])
    #%%
    #indexes dos mesmos setores

    sectors = frame['Sector'].unique()
    sector_num=sectors.shape[0]
    sectors_indexes = {}
    for sector in sectors:
        sector_index = f"{sector}_index"
        sector_list = np.where(frame['Sector'] == sector)[0]
        sectors_indexes[sector_index] =  sector_list
    #%%
    # cria matria de coefientes de restricoes A

    A_num_colunas=frame.shape[0]
        # numero vars de decisao
    A_num_linhas = 1 + sectors.shape[0]
        # restricao recurso total = 1
        # restricao recurso para cada setor = numero setores
        
    A0 = np.zeros([A_num_linhas,A_num_colunas])

    A0[0,:]= frame['Current Price'] # coefientes para restricao de recursos total

    i = 1
    ordem_setores=[]
    for sector in sectors_indexes:
        ordem_setores.append(sector)
        for index in sectors_indexes[sector]:
            A0[i,index] = frame['Current Price'][index] # coefientes para restricao de cada setor
        i+=1
       
    b= criar_b(investimento, proporcao_limite_por_setor,sector_num)
        # cria vetor b
    
#%%    
    # Cria problema de maximizacao
    problem = LpProblem("Large LP", LpMaximize)
    
    # Define numero vars e restricoes
    num_variables = A0.shape[1]
    num_constraints = A0.shape[0]

    # Cria variaveis
    ativos = frame['Symbol']
    variables = [LpVariable(f'{ativos[i]}', lowBound=0,upBound=(proporcao_limite_por_ativo[i]*investimento/A0[0][i]), cat=LpInteger) for i in range(num_variables)]

    # Define funcao objetivo
    if investimento_total_anterior[0] != 0:
        
        proporcao_carteira_anterior=[]
        
        for i in range(num_variables):
            vetor_valor_anterior = vetor_valor_anterior.reshape(A_num_colunas,1)
            proporcao_carteira_anterior.append(((A0[0][i]* vetor_valor_anterior[i] ) /investimento_total_anterior )[0])
        
    
    else:
        proporcao_carteira_anterior=np.zeros(A_num_colunas)
    
    objective_coeffs = [indice_sharpe_obj[i][0][0]*(1-proporcao_carteira_anterior[i]) for i in range(num_variables)]

    problem += sum(variables[i] * objective_coeffs[i] for i in range(num_variables)) #adiciona funcao obj ao problema

    # Adiciona restricoes
    for j in range(num_constraints):
        constraint_coeffs = [A0[j][i] for i in range(num_variables)]
        constraint = sum(variables[i] * constraint_coeffs[i] for i in range(num_variables)) <= b[j]
        problem += constraint
    
    # Selecionar solver Branch n Cut
    solver = pulp.PULP_CBC_CMD(msg=False)
    
    # Resolver o problema inteiro
    problem.solve(solver)

    # Print the status of the solution
  #  print("Status:", LpStatus[problem.status])

    var_value=[]
    for variable in variables:
        var_value.append((f"{variable.name} = {variable.value()}"))

    value_dic = {s.split(' = ')[0]: float(s.split(' = ')[1]) for s in var_value}

    vetor_valor=np.array([ value_dic[key] for key in value_dic ]).reshape(frame.shape[0],1)

    retorno_esperado = np.transpose(np.array(previsao_not_norm).reshape(frame.shape[0],1))@vetor_valor #retorno bruto
    
    portifolio_dic={}
    for key in value_dic:
        if value_dic[key] != 0:
            portifolio_dic[key] = value_dic[key]
            
    gasto =  np.transpose(np.array(frame['Current Price']).reshape(frame.shape[0],1))@vetor_valor
    
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


    variacao_portifolio = np.transpose(np. array(vetor_peso_ativos).reshape(frame.shape[0],1)) @ matriz_cor @ np.array(vetor_peso_ativos)
    volatilidade_portifolio = np.sqrt(variacao_portifolio)
    
    retorno= retorno_esperado/gasto-1 #fracao em relacao ao gasto
    
    indice_sharpe=retorno/volatilidade_portifolio
    

    return portifolio_dic, retorno_esperado, gasto, volatilidade_portifolio, indice_sharpe,retorno,vetor_valor_acumulado,investimento_total_acumulado,proporcao_carteira_atualizado,proporcao_carteira_iteracao
#%%
