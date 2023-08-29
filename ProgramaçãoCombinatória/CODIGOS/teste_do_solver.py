# -*- coding: utf-8 -*-
"""
Created on Fri May 19 18:43:49 2023

@author: Nick
"""

import numpy as np
from sklearn.linear_model import LinearRegression
import pulp
from pulp import LpProblem, LpVariable, LpInteger, LpMaximize, LpStatus
# Cria problema de maximizacao

problem = LpProblem("Large LP", LpMaximize)

# Define numero vars e restricoes
num_variables = 2
num_constraints = 2

# Cria variaveis

variables = [LpVariable(f'{i}', lowBound=0,cat=LpInteger) for i in range(num_variables)]

# Define funcao objetivo

objective_coeffs = [ 5, -1]

problem += sum(variables[i] * objective_coeffs[i] for i in range(num_variables)) #adiciona funcao obj ao problema

# Adiciona restricoes
A0 = [[7,-5] , [3,2]]
b = [13,17]
for j in range(num_constraints):
    constraint_coeffs = [A0[j][i] for i in range(num_variables)]
    constraint = sum(variables[i] * constraint_coeffs[i] for i in range(num_variables)) <= b[j]
    problem += constraint

# Selecionar solver Branch n Cut
solver = pulp.PULP_CBC_CMD(msg=False)

# Resolver o problema inteiro
problem.solve(solver)
var_value=[]
for variable in variables:
    var_value.append((f"{variable.name} = {variable.value()}"))