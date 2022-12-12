# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 18:31:26 2022

@author: Nick
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
from random import randint
import scipy 
from scipy import optimize

X = np.array(pd.read_csv(r"C:/Users/accam/Documents/MS571/Projeto1_/imageMNIST.csv",decimal=','))
y = np.array(pd.read_csv(r"C:/Users/accam/Documents/MS571/Projeto1_/labelMNIST.csv"))

#%%sigmoide

def sigmoid(z):
    return 1/(1+np.exp(-z))


#%%gradiente sigmoide


def sigmoidGradient(z):
    sigmoid = 1/(1+np.exp(-z))
    return sigmoid*(1-sigmoid)


#%%custo + gradiente

def computeCost(X,y,theta,input_layer_size,hidden_layer_size,num_labels, Lambda):
    theta1 = theta[:((input_layer_size+1)*hidden_layer_size)].reshape(hidden_layer_size,input_layer_size+1)
    theta2 = theta[((input_layer_size+1)*hidden_layer_size):].reshape(num_labels,hidden_layer_size+1)
    
    m = X.shape[0]
    J = 0
    X = np.hstack((np.ones((m,1)),X))
    y10 = np.zeros((m,num_labels))
    
    a1 = sigmoid(X @ theta1.T)
    a1 = np.hstack((np.ones((m,1)),a1))
    a2 = sigmoid(a1 @ theta2.T)
    
    for i in range(1,num_labels+1):
        y10[:,i-1][:,np.newaxis] = np.where(y==i,1,0)
    for j in range(num_labels):
        J = J + sum(-y10[:,j]*np.log(a2[:,j])-(1-y10[:,j])*np.log(1-a2[:,j]))
        
    cost = 1/m*J
    reg_J = cost + Lambda/(2*m)*(np.sum(theta1[:,1:]**2)+np.sum(theta2[:,1:]**2))
                                 
    grad1 = np.zeros((theta1.shape))
    grad2 = np.zeros((theta2.shape))
                                 
    for i in range(m):
        xi = X[i,:]
        a1i = a1[i,:]
        a2i = a2[i,:]
        d2 = a2i - y10[i,:]
        d1 = theta2.T @ d2.T * sigmoidGradient(np.hstack((1,xi @ theta1.T)))
        grad1 = grad1 + d1[1:][:,np.newaxis]@xi[:,np.newaxis].T
        grad2 = grad2 + d2.T[:,np.newaxis]@a1i[:,np.newaxis].T
                                 
    grad1 = 1/m*grad1
    grad2 = 1/m*grad2
                                 
    grad1_reg = grad1 + (Lambda/m)*np.hstack((np.zeros((theta1.shape[0],1)),theta1[:,1:]))
    grad2_reg = grad2 + (Lambda/m)*np.hstack((np.zeros((theta2.shape[0],1)),theta2[:,1:]))
                                 
    return cost,grad1,grad2,reg_J,grad1_reg,grad2_reg


#%%inicializacao parametros


def randInitializeWeights(L_in,L_out):
    epi = (6**1/2)/(L_in+L_out)**1/2
    W = np.random.rand(L_out,L_in+1)*(2*epi)-epi
    return W


#%%gradiente descendente


def gradientDescent(X,y,theta,alpha,nbr_iter,Lambda,input_layer_size,hidden_layer_size,num_labels):#regularizado
    theta1 = theta[:((input_layer_size+1)*hidden_layer_size)].reshape(hidden_layer_size,input_layer_size+1)
    theta2 = theta[((input_layer_size+1)*hidden_layer_size):].reshape(num_labels,hidden_layer_size+1)
    
    J_history_reg = []
    
    for i in range(nbr_iter):
        theta = np.append(theta1.flatten(),theta2.flatten())
        cost,grad1,grad2 = computeCost(X,y,theta,input_layer_size,hidden_layer_size,num_labels,Lambda)[3:]#pegando regularizado
        theta1 = theta1 - (alpha*grad1)
        theta2 = theta2 - (alpha*grad2)
        J_history_reg.append(cost)
        
    nn_paramsFinal = np.append(theta1.flatten(),theta2.flatten())
    return nn_paramsFinal,J_history_reg


#%%presicao


def prediction(X,theta1,theta2):
    m = X.shape[0]
    X = np.hstack((np.ones((m,1)),X))
    
    a1 = sigmoid(X @ theta1.T)
    a1 = np.hstack((np.ones((m,1)),a1))
    a2 = sigmoid(a1 @ theta2.T)
    
    return np.argmax(a2,axis=1)+1


#%%teste 1


input_layer_size = 400
hidden_layer_size = 25
num_labels = 10

initial_theta1 = randInitializeWeights(input_layer_size,hidden_layer_size)
initial_theta2 = randInitializeWeights(hidden_layer_size,num_labels)
initial_theta = np.append(initial_theta1.flatten(),initial_theta2.flatten())

theta,J_history = gradientDescent(X,y,initial_theta,0.8,1000,1,input_layer_size,hidden_layer_size,num_labels)#1000 iter, alpha 1, lmba 1
theta1 = theta[:((input_layer_size+1)*hidden_layer_size)].reshape(hidden_layer_size,input_layer_size+1)
theta2 = theta[((input_layer_size+1)*hidden_layer_size):].reshape(num_labels,hidden_layer_size+1)


#%%

pred = prediction(X,theta1,theta2)
print("Taxa de acerto:",sum(pred[:,np.newaxis]==y)[0]/5000*100,"%")

#%%
#ver quais estao errados

errado = []
certo = []

m = X.shape[0]
pred = pred.reshape(m,1)
y = y.reshape(m,1)

for i in range(m):
    if pred[i]!=y[i]:
        errado.append(pred[i][0])
        certo.append(y[i][0])
        
table=(np.array([errado,certo])).T
rows=[]
for i in range(table.shape[0]):
    rows.append("Erro "+str(i+1))
colunas=["Errado","Certo"]
tabela=pd.DataFrame(table,index=rows,columns=colunas)
print(tabela)

#%%
#grafico da funcao custo

plt.plot(J_history)
plt.xlabel('número iterações'), plt.ylabel('custo')
plt.title("# iterações x custo")
plt.show()


#%% 
#comparar gradiente do back com a aproximacao

exemplos_teste=[randint(0,400),randint(0,400),randint(0,400)]
atributos_teste = [randint(0,400),randint(0,400),randint(0,400)]

X_teste = list()

for i in range(3):
    for j in range (3):
        X_teste.append(X[exemplos_teste[i]][atributos_teste[j]])

X_teste = np.array(X_teste)
X_teste = X_teste.reshape(3,3)

epsilon = 10**(-4)

y_teste=[y[exemplos_teste][0],y[exemplos_teste][1],y[exemplos_teste][2]]
y_teste=np.array(y_teste)
y_teste=y_teste.reshape(3,1)

input_layer_size = 3
hidden_layer_size = 5
num_labels = 3

initial_theta1 = randInitializeWeights(input_layer_size,hidden_layer_size)
initial_theta2 = randInitializeWeights(hidden_layer_size,num_labels)
initial_theta = np.append(initial_theta1.flatten(),initial_theta2.flatten())
 

grad1,grad2 = computeCost(X_teste,y_teste,initial_theta,input_layer_size,hidden_layer_size,num_labels, 1)[1], computeCost(X_teste,y_teste,initial_theta,input_layer_size,hidden_layer_size,num_labels, 1)[2]


def grad_teste(X,y,theta,input_layer_size,hidden_layer_size,num_labels, epsilon):
    
    t = len(initial_theta)
    m = X.shape[0]
    X = np.hstack((np.ones((m,1)),X))
    y10 = np.zeros((m,num_labels))
    for i in range(num_labels+1):
        y10[:,i-1][:,np.newaxis] = np.where(y==i,1,0)   
    grad=[]
    
    theta1 = theta[:((input_layer_size+1)*hidden_layer_size)]
    theta2 = theta[((input_layer_size+1)*hidden_layer_size):]
    
  
    for t in range(len(theta)):      
        
        J1 = 0
        J2 = 0
        theta[t]= theta[t]+epsilon
        
        theta1 = theta[:((input_layer_size+1)*hidden_layer_size)]
        theta2 = theta[((input_layer_size+1)*hidden_layer_size):]
        theta1 = theta1.reshape(hidden_layer_size,input_layer_size+1)
        theta2 = theta2.reshape(num_labels,hidden_layer_size+1)
        
                
        a1 = sigmoid(X @ theta1.T)       
        a1 = np.hstack((np.ones((m,1)),a1))
        a2 = sigmoid(a1 @ theta2.T)        
 
        for j in range(num_labels):
            J1 = J1 + sum(-y10[:,j]*np.log(a2[:,j])-(1-y10[:,j])*np.log(1-a2[:,j]))
        
        theta[t]= theta[t]-2*epsilon
        
        theta1 = theta[:((input_layer_size+1)*hidden_layer_size)]
        theta2 = theta[((input_layer_size+1)*hidden_layer_size):]
        theta1 = theta1.reshape(hidden_layer_size,input_layer_size+1)
        theta2 = theta2.reshape(num_labels,hidden_layer_size+1)
        
        a1 = sigmoid(X @ theta1.T)       
        a1 = np.hstack((np.ones((m,1)),a1))
        a2 = sigmoid(a1 @ theta2.T)     
        for j in range(num_labels):
            J2 = J2 + sum(-y10[:,j]*np.log(a2[:,j])-(1-y10[:,j])*np.log(1-a2[:,j]))
            
        
        grad_theta_j_i = (J1-J2)/(2*epsilon)
        
        
        grad.append(grad_theta_j_i)
      
    grad1=grad[:((input_layer_size+1)*hidden_layer_size)]
    grad2=grad[((input_layer_size+1)*hidden_layer_size):]
    grad1=np.array(grad1).reshape(hidden_layer_size,input_layer_size+1)
    grad2=np.array(grad2).reshape(num_labels,hidden_layer_size+1)
    grad1=1/m*grad1
    grad2=1/m*grad2
    
    return grad1, grad2

grad1_aprox, grad2_aprox= grad_teste(X_teste,y_teste,initial_theta,input_layer_size,hidden_layer_size,num_labels, epsilon)[0], grad_teste(X_teste,y_teste,initial_theta,input_layer_size,hidden_layer_size,num_labels, epsilon)[1]

print("Quadrado da diferença das normas do grad1:",(np.linalg.norm(grad1)-np.linalg.norm(grad1_aprox))**2)
print("Quadrado da diferença das normas do grad2:",(np.linalg.norm(grad2)-np.linalg.norm(grad2_aprox))**2)

#%%
#grad conjugado

input_layer_size = 400
hidden_layer_size = 25
num_labels = 10

value_grad_conj_iteracoes=[]
iteracoes=np.linspace(100,400,4)
lmbda=[0,0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1, 3, 10.] 
initial_theta1 = randInitializeWeights(input_layer_size,hidden_layer_size)
initial_theta2 = randInitializeWeights(hidden_layer_size,num_labels)
initial_theta = np.append(initial_theta1.flatten(),initial_theta2.flatten())
#%%funcoes para grad conju
def fun(theta,lmbda):
    X = np.array(pd.read_csv(r"C:/Users/accam/Documents/MS571/Projeto1_/imageMNIST.csv",decimal=','))
    theta1 = theta[:((input_layer_size+1)*hidden_layer_size)].reshape(hidden_layer_size,input_layer_size+1)
    theta2 = theta[((input_layer_size+1)*hidden_layer_size):].reshape(num_labels,hidden_layer_size+1)
    
    m = X.shape[0]
    J = 0
    X = np.hstack((np.ones((m,1)),X))
    y10 = np.zeros((m,num_labels))
    
    a1 = sigmoid(X @ theta1.T)
    a1 = np.hstack((np.ones((m,1)),a1))
    a2 = sigmoid(a1 @ theta2.T)
    
    for i in range(1,num_labels+1):
        y10[:,i-1][:,np.newaxis] = np.where(y==i,1,0)
    for j in range(num_labels):
        J = J + sum(-y10[:,j]*np.log(a2[:,j])-(1-y10[:,j])*np.log(1-a2[:,j]))
        
    return 1/m*J + lmbda/(2*m)*(np.sum(theta1[:,1:]**2)+np.sum(theta2[:,1:]**2))

def jac(theta,lmbda):
    theta1 = theta[:((input_layer_size+1)*hidden_layer_size)].reshape(hidden_layer_size,input_layer_size+1)
    theta2 = theta[((input_layer_size+1)*hidden_layer_size):].reshape(num_labels,hidden_layer_size+1)
    X = np.array(pd.read_csv(r"C:/Users/accam/Documents/MS571/Projeto1_/imageMNIST.csv",decimal=','))                           
    grad1 = np.zeros((theta1.shape))
    grad2 = np.zeros((theta2.shape))
    m = X.shape[0]
    X = np.hstack((np.ones((m,1)),X))
    y10 = np.zeros((m,num_labels))
    
    a1 = sigmoid(X @ theta1.T)       
    a1 = np.hstack((np.ones((m,1)),a1))
    a2 = sigmoid(a1 @ theta2.T)        

                                 
    for i in range(m):
        xi = X[i,:]
        a1i = a1[i,:]
        a2i = a2[i,:]
        d2 = a2i - y10[i,:]
        d1 = theta2.T @ d2.T * sigmoidGradient(np.hstack((1,xi @ theta1.T)))
        grad1 = grad1 + d1[1:][:,np.newaxis]@xi[:,np.newaxis].T
        grad2 = grad2 + d2.T[:,np.newaxis]@a1i[:,np.newaxis].T
                                 
    grad1 = 1/m*grad1
    grad2 = 1/m*grad2
                                 
    grad1_reg = grad1 + (lmbda/m)*np.hstack((np.zeros((theta1.shape[0],1)),theta1[:,1:]))
    grad2_reg = grad2 + (lmbda/m)*np.hstack((np.zeros((theta2.shape[0],1)),theta2[:,1:]))
    grad = np.append(grad1_reg.flatten(),grad2_reg.flatten())
    return grad
#%%teste com CG variando lambda
custo_GC_per_lmbda=[]
#GC_iter=[]
for i in range(len(lmbda)):
    
    CG = scipy.optimize.minimize(fun, initial_theta,args=(lmbda[i]), method='CG', jac=jac)
    custo_GC_per_lmbda.append(CG['fun'])
   # GC_iter.append(CG['nit'])

plt.plot(lmbda,custo_GC_per_lmbda)
plt.xlabel('lmbda'), plt.ylabel('custo')
plt.title("lmbda x custo")
plt.show()

index_melhor_lmbda= custo_GC_per_lmbda.index(min(custo_GC_per_lmbda))
melhor_lmbda = iteracoes[index_melhor_lmbda]
'''
plt.plot(GC_iter,custo_GC_per_lmbda)
plt.xlabel('iters'), plt.ylabel('custo')
plt.title("iters x custo")
plt.show()


#%%

value_grad_conj_iteracoes=[]
for i in range(len(iteracoes)):
    
    CG = scipy.optimize.minimize(fun, initial_theta,args=(melhor_lmbda), method='CG', jac=jac,options={'maxiter':iteracoes[i]})
    value_grad_conj_iteracoes.append(CG['fun'])

#%%

CG1 = CG[:((input_layer_size+1)*hidden_layer_size)].reshape(hidden_layer_size,input_layer_size+1)
CG2 = CG[((input_layer_size+1)*hidden_layer_size):].reshape(num_labels,hidden_layer_size+1)
pred = prediction(X,CG1,CG2)

plt.plot(iteracoes,value_grad_conj_iteracoes)
plt.xlabel('número iterações'), plt.ylabel('custo')
plt.title("# iterações x custo")
plt.show()
index_melhor_iter= value_grad_conj_iteracoes.index(min(value_grad_conj_iteracoes))
melhor_iter = iteracoes[index_melhor_iter]
print("Melhor numero de iter para grad conj:",melhor_iter, "com custo de: ", value_grad_conj_iteracoes[index_melhor_iter])
'''
#%% imagens dos thetas da 1 camada

theta1_nobias = np.delete(theta1,slice(1),1)
imagens_theta =[]

for j in range(theta1_nobias.shape[0]):
    for i in range(theta1_nobias.shape[1]):
        theta1_nobias[j][i] = (theta1_nobias[j][i] - np.mean(theta1_nobias[j]))/ np.std(theta1_nobias[j])
        
    theta_imagem = theta1_nobias[j].reshape(20,20)
    imagens_theta.append(theta_imagem )
#%%    
for i in range(len(imagens_theta)):
    
    plt.imshow((imagens_theta[i]).reshape(20,20),cmap='hot')
    plt.colorbar()
    plt.show()
    
#%%holdout
def holdout(X,Y,p1,p2):#porcewntagens de treino e validacao que quer separar
    m = X.shape[0]
    Y=y
    m_treino = np.array(random.sample(range(0, m), round(m*p1/100)))#linhas para o ex de 

    x_treino=[]
    y_treino=[]

    for i in range(len(m_treino)):
        x_treino.append(X[m_treino[i]])
    x_treino = np.array(x_treino)


    for i in range(len(m_treino)):
        y_treino.append(y[m_treino[i]])
    y_treino = np.array(y_treino)

    linhas_mesmo_elem=[[],[],[],[],[],[],[],[],[],[]]
    for i in range(len(m_treino)):
        for j in range(1,11):
            if y_treino[i] == j:
                linhas_mesmo_elem[j-1].append(i)

    porporcao_label = []
    for i in range(len(linhas_mesmo_elem)):
        porporcao_label.append(len(linhas_mesmo_elem[i])/m_treino.shape[0])

    lista_remover=list(m_treino)
    X1=np.delete(X,lista_remover, axis=0)#X dps de tirar o treino
    Y1=np.delete(Y,lista_remover, axis=0)
    m1 = X1.shape[0]
    m_val=round(m*p2/100)

    n_labels_val=[]

    for i  in range(len(porporcao_label)):
        n_labels_val.append(round(m_val*porporcao_label[i]))

        

    linhas_mesmo_elem1=[[],[],[],[],[],[],[],[],[],[]]
    for i in range(m1):
        for j in range(1,11):
            if Y1[i] == j:
                linhas_mesmo_elem1[j-1].append(i)      
                
             
    list_m_val=[[],[],[],[],[],[],[],[],[],[]]   #exemplos de validacao separados por cada label

    for i in range(len(n_labels_val)):
        n=np.array(random.sample(range(0, len(linhas_mesmo_elem1[i])), n_labels_val[i]))
        for j in range(len(n)):
            list_m_val[i].append(linhas_mesmo_elem1[i][n[j]])

    list_m_val=np.array(list_m_val,dtype=object)

       
    x_val=[]
    for i in range(len(list_m_val)):
        for j in range(len(list_m_val[i])):
            x_val.append(X1[list_m_val[i][j]])  
    x_val = np.array(x_val)

    y_val=[]
    for i in range(len(list_m_val)):
        for j in range(len(list_m_val[i])):
            y_val.append(Y1[list_m_val[i][j]])        
    y_val = np.array(y_val)

    lista_remover=[]
    for i in range(len(list_m_val)):
        for j in range(len(list_m_val[i])):
            lista_remover.append(list_m_val[i][j])        

    X_teste=np.delete(X1,lista_remover, axis=0)#
    Y_teste=np.delete(Y1,lista_remover, axis=0)
    
    return (x_treino,y_treino),(x_val,y_val),(X_teste,Y_teste)   

#%%melhor lmbda atraves da validacao
def find_lbda(X,y,hiperpar,pt,pv, k):#k holdouts
    
    err_validacao=[]
    for i in range(len(hiperpar)):
        erro=0
        for j in range(k):           
            initial_theta1 = randInitializeWeights(input_layer_size,hidden_layer_size)
            initial_theta2 = randInitializeWeights(hidden_layer_size,num_labels)
            initial_theta = np.append(initial_theta1.flatten(),initial_theta2.flatten())
            sample=holdout(X,y,pt,pv)
            xtreino,ytreino,xval,yval,xtest,yteste= sample[0][0],sample[0][1],sample[1][0],sample[1][1],sample[2][0],sample[2][1]
            treino=gradientDescent(xtreino,ytreino,initial_theta,alpha,iteracoes,hiperpar[i],input_layer_size,hidden_layer_size,num_labels)
            custo_val=computeCost(xval,yval,treino[0],input_layer_size,hidden_layer_size,num_labels, 0)[0]
            erro+=custo_val
        err_validacao.append(erro/k)
        
    index_menor_erro_val= err_validacao.index(min(err_validacao))
    melhor_lbda = hiperpar[index_menor_erro_val]
    
    x_,y_=np.append(xtreino,xval,axis=0),np.append(ytreino,yval,axis=0)
    treino=gradientDescent(x_,y_,initial_theta,alpha,iteracoes,melhor_lbda,input_layer_size,hidden_layer_size,num_labels)#treino novo pro teste
    custo_teste=computeCost(xtest,yteste,treino[0],input_layer_size,hidden_layer_size,num_labels, 0)[0]
    return melhor_lbda, custo_teste,err_validacao
#%%curvas de aprendizado
def curva_aprendizado(X,y,p1,p2,lbda,k):
    treino_custo=[]
    val_custo=[]
    for i in range(len(p1)):
        erro1,erro2=0,0
        for j in range(k):
            initial_theta1 = randInitializeWeights(input_layer_size,hidden_layer_size)
            initial_theta2 = randInitializeWeights(hidden_layer_size,num_labels)
            initial_theta = np.append(initial_theta1.flatten(),initial_theta2.flatten())
            sample=holdout(X,y,p1[i],p2[i])
            xtreino,ytreino,xval,yval= sample[0][0],sample[0][1],sample[1][0],sample[1][1]
            treino=gradientDescent(xtreino,ytreino,initial_theta,alpha,iteracoes,lbda,input_layer_size,hidden_layer_size,num_labels)#regularizado
            custo_treino=computeCost(xtreino,ytreino,treino[0],input_layer_size,hidden_layer_size,num_labels, 0)[0]
            erro1+=custo_treino
            custo_val=computeCost(xval,yval,treino[0],input_layer_size,hidden_layer_size,num_labels, 0)[0]
            erro2+=custo_val
        treino_custo.append(erro1/k)
        val_custo.append(erro2/k)
    return treino_custo,val_custo

#%%testes gerais
alpha=0.8
hiperpar=[0,0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1, 3, 10.] 
p1=np.linspace(10, 90,18) #de 10 a 90% de treino variando em 5%
#p1=np.linspace(10, 90,2)
p2=(100-p1)/2
input_layer_size = 400
hidden_layer_size = 25
num_labels = 10
iteracoes=1000
#iteracoes=10
k=10
#k = 2
#%%achar melhor lmbda,custo teste desse lbds, erro de validacao em funcao de lbds
pt,pv=60,20 #60% TREINO 20% VALIDACAO

l,custo_teste,err_val=find_lbda(X,y,hiperpar,pt,pv,k)
#%%
plt.plot(hiperpar,err_val) 
plt.scatter(hiperpar,err_val) 
plt.xlabel('lmbda'), plt.ylabel('erro val')  
plt.title("lmbda x erro validacao")
plt.show()
print("Melhor lmbda:",l,", com erro de teste de:",custo_teste)
 #%%
 
plt.plot(hiperpar[:5],err_val[:5]) 
plt.scatter(hiperpar[:5],err_val[:5]) 
plt.xlabel('lmbda'), plt.ylabel('erro val')  
plt.title("lmbda x erro validacao")
plt.show()

#%%#%%curva de aprendizado
treino_custo,val_custo=curva_aprendizado(X,y,p1,p2,l,k)
treino_=plt.plot(p1,treino_custo,label="treino")
val_= plt.plot(p1,val_custo,label="val")
plt.xlabel('% treino'), plt.ylabel('erro')
plt.title("Curva de Aprendizado")
leg = plt.legend()
plt.show()
