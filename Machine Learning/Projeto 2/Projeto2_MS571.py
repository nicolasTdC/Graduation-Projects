# -*- coding: utf-8 -*-
import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt
import scipy.optimize as spy
import pandas as pd

#%%PARTE I
dado1 = loadmat("dado1.mat")
X = dado1["X"]
m=X.shape[0]
n=X.shape[1]
#%%100 imagens de X
fig,axis = plt.subplots(10,10,figsize=(8,8))
M=np.random.randint(m,size=100)
p=0
for i in range(10):
    for j in range(10):
        axis[i,j].imshow(X[M[p],:].reshape(32,32,order="F"),cmap="Greys")
        axis[i,j].axis("off")
        p+=1
plt.show()
#%%
def PCA1(X,m,n):
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
            
    Sigma=1/m*X.T@X#matriz cov

    U,S,V=np.linalg.svd(Sigma)#autovetores
    
    return mean,std,U,S
#%%
def PCA2(U,S,er):
    
    for k in range(U.shape[1]):
        
        var_check=sum(S[:k])/sum(S)
        
        if var_check>=1-er:
            break
        
    U_red=U[:,0:k]
               

    Z=X@U_red #atributos redimensionados
    return U_red,Z
#%%PCA
def PCA(X,m,n,er):
    mean,std,U,S=PCA1(X,m,n)
    U_red,Z=PCA2(U,S,er)
    return mean,std,U,U_red,Z
#%%reducao de X
mean,std,U,U_red,Z=PCA(X,m,n,0.01)
#%%eigenfaces
eig=U[:,:36].T

fig,axis = plt.subplots(6,6,figsize=(8,8))

p=0
for i in range(6):
    for j in range(6):
        axis[i,j].imshow(eig[p,:].reshape(32,32,order="F"),cmap="Greys")
        axis[i,j].axis("off")
        p+=1
plt.show()
#%%sobre 100 componentes principais
mean,std,U,S=PCA1(X,m,n)
U_red=U[:,:100]
Z=X@U_red

X_ap=Z@U_red.T

#%%100 faces de X
fig,axis = plt.subplots(10,10,figsize=(8,8))
p=0
for i in range(10):
    for j in range(10):
        axis[i,j].imshow(X[p,:].reshape(32,32,order="F"),cmap="Greys")
        axis[i,j].axis("off")
        p+=1
plt.show()
#%%100 faces de X_ap
fig,axis = plt.subplots(10,10,figsize=(8,8))
p=0
for i in range(10):
    for j in range(10):
        axis[i,j].imshow(X_ap[p,:].reshape(32,32,order="F"),cmap="Greys")
        axis[i,j].axis("off")
        p+=1
plt.show()

#%%PARTE II
mat = loadmat("dado2.mat")
Y = mat['Y']
R=mat['R']

num_x,num_theta=100,100
num_filmes,num_users=Y.shape[0],Y.shape[1]

#inicializacao aleatoria dos features e params
X = np.random.randn(num_filmes, num_x)
Theta = np.random.randn(num_users, num_x)
initial_parameters = np.append(X.flatten(),Theta.flatten())
#%%funcao custo e gradiente, e normalizar notas

def  cost_jac(params, Y, R, num_users, num_filmes, num_x):
        
    X = params[:num_filmes*num_x].reshape(num_filmes,num_x)
    Theta = params[num_filmes*num_x:].reshape(num_users,num_x)
    
    predictions =  X @ Theta.T
    err = (predictions - Y)
    J = 1/2 * np.sum((err**2) * R)   
    X_grad = err*R @ Theta
    Theta_grad = (err*R).T @ X
    grad = np.append(X_grad.flatten(),Theta_grad.flatten())
    
    
    return J,grad


def Notas_Normal(Y, R):
    
    m,n = Y.shape[0], Y.shape[1]
    Ymean = np.zeros((m,1))
    Ynorm = np.zeros((m,n))
    
    for i in range(m):
        Ymean[i] = np.sum(Y[i,:])/np.count_nonzero(R[i,:])
        Ynorm[i,R[i,:]==1] = Y[i,R[i,:]==1] - Ymean[i]
        
    return Ynorm, Ymean
#%%treino
Ynorm, Ymean = Notas_Normal(Y, R)

GC=spy.minimize(cost_jac,initial_parameters,args=(Ynorm, R, num_users, num_filmes, num_x),method='CG',jac=True,options={'maxiter': None})

pars=GC['x']

X = pars[:num_filmes*num_x].reshape(num_filmes,num_x)
Theta = pars[num_filmes*num_x:].reshape(num_users,num_x)
#%%predicao
pred =X@Theta.T + Ymean

notas_medias=[]
for i in range(pred.shape[0]):
    nota_media=np.sum(pred[i,:]*R[i,:])/np.sum(R[i,:])
    notas_medias.append(nota_media)

#%%
movieList = open("dado3.txt","r").read().split("\n")[:-1]
df = pd.DataFrame(np.hstack((np.array(notas_medias)[:,np.newaxis],np.array(movieList)[:,np.newaxis])))
df.sort_values(by=[0],ascending=False,inplace=True)
df.reset_index(drop=True,inplace=True)

print("10 filmes com notas médias mais altas:\n")
for i in range(10):
    print("Nota predita",round(float(df[0][i]),2)," para o filme:",df[1][i])
