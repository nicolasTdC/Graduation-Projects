# -*- coding: utf-8 -*-
import numpy as np
#%%checar funcao
def check_fun(Xb,C_B,C_N,idx_B,idx_N):
    fun = ((np.array(C_B)).reshape(1,len(C_B)))@Xb
    return fun
#%%custos relativos
def custos_rel(B,N,C_B,C_N,idx_B,idx_N):
        
    Xb=np.linalg.solve(B,b)#sol basica
    lmbda = np.linalg.solve(B.T,C_B)
    custos_rel=[]
    for i in range(len(idx_N)):
        cost=C_N[i]-(lmbda.T)@N[:,i]
        custos_rel.append(cost)
    
    Ck=min(custos_rel)
    
    if Ck>=0:     
        return 1,Xb,B,N,C_B,C_N,idx_B,idx_N
    
    else:
        
        idx_min=custos_rel.index(Ck)
        entrar=idx_N[idx_min]#indice coluna/var para entrar
        
        #direcao
        D=np.linalg.solve(B,N[:,idx_min])
        if max(D)<=0:
            return 2,Xb,B,N,C_B,C_N,idx_B,idx_N#print("Problema não tem solucao ́otima finita.")
       #   print("lol")
        else:
            passo=[]
            for i in range(len(D)):
                if D[i] <= 0:
                    passo.append(-1)
                else:
                    epsilon=float(Xb[i]/D[i])
                    passo.append(epsilon)
            for i in range(len(passo)):
                if passo[i] == -1:
                    passo[i]  = 2*max(passo)
            passo_min=min(passo)
            sair=passo.index(passo_min)#indice idx_B a sair
            
            #atualizacao de Base
            N_,B_= np.array(N[:,entrar]), np.array(B[:,sair]) #vars recipientes
            B[:,sair] = N_#base atualizada
            N[:,entrar] = B_#nao base atualizada
            idx_N_,idx_B_=int(idx_N[entrar]),int(idx_B[sair])#vars recipientes
            idx_B[sair]=idx_N_
            idx_N[entrar]=idx_B_
            CN_,CB_ = (C_N.copy())[entrar], (C_B.copy())[sair]
            #CN_,CB_ = np.array(C_N[entrar,0]), np.array(C_B[sair,0])
            C_N[entrar]=CB_  
            C_B[sair]=CN_

        
            return 0,Xb,B,N,C_B,C_N,idx_B,idx_N
#%%problema artificial

def prob_artf(m,n,nbr_aux,lista_m,flag_m,B,idx_B,idx_N):
        c_aux=np.zeros((n+nbr_aux,1))
        idx=[]
        for i in range(len(lista_m)):
            if lista_m[i] in flag_m:
                idx.append(i)
            aux_m=np.delete(lista_m,idx)  #linhas pros 1 da identidade artficial
    
        aux=[] #colunas artificiais
        for i in range(len(aux_m)):
            indice=int(aux_m[i])
            column_artf= np.zeros((m,1))
            column_artf[indice]=1
            aux.append(column_artf)
        A_aux=aux[0]
        if(len(aux))>1:
            
            for i in range(1,len(aux)):
                A_aux=np.hstack((A_aux,aux[i]))#matriz colunas artificiais

        if len(B)!=0:
            
            B=np.hstack((B.reshape(m,len(idx_B)),A_aux.reshape(m,nbr_aux)))   
        else:
            B=A_aux.reshape(m,nbr_aux)
    
        idx_artf=[]#indices para var artificiais
        for i in range(nbr_aux):
            idx_artf.append(n+i)
    
        for i in range(nbr_aux):
            idx_B.append(idx_artf[i])
            c_aux[idx_artf[i]]=1
    
        C_B=[]#custo B
        C_N=[]#custo N
        for i in idx_B:
            C_B.append(c_aux[i])
            
        for i in idx_N:    
            C_N.append(c_aux[i])
    
        C_B,C_N=(np.array(C_B)).reshape(len(idx_B),1),(np.array(C_N)).reshape(len(idx_N),1)
            
        
        return B,C_B, C_N, idx_B, idx_N,idx_artf
#%%particao
def particao(A,c,m,n):    
    idx_B=[]#indices colunas idx_B
    idx_N=[]#indices colunas n idx_B
    flag_m=[]#linhas do 1 da identidade
    lista_n=np.linspace(0,n-1,n)#lista de 0 a n-1
    lista_m=np.linspace(0,m-1,m)#lista de 0 a m-1

    for i in range(n):#analisando indexes para idx_B
        if len(idx_B) == m:
            break    
        flag1=0
        flag0=0
        for j in range(m):
            if A[j][i] == 0 : 
                flag0+=1
                continue
            elif A[j][i] == 1:
                if j not in flag_m:
                    if flag1==0:
                        flag_m.append(j)      
                        flag1 = flag1+1
                    continue
                
        if (flag1 == 1) and (flag0==(m-1)):
            idx_B.append(i)
        elif (flag1 == 1) and (flag0!=(m-1)) :
            if len(flag_m)>0:
                
                flag_m.remove(flag_m[-1])

    for i in range(len(lista_n)):
        if lista_n[i] not in idx_B:
            idx_N.append(i)

    BASE_columns=[]
    for i in range(len(idx_B)):
        BASE_columns.append(A[:,idx_B[i]])
        
    if len(idx_B)>1:  
        B=BASE_columns[0].reshape(m,1)
        for i in range(1,len(idx_B)):
            B=np.hstack((B,BASE_columns[i].reshape(m,1)))
    elif len(idx_B)==1:
        B=BASE_columns[0]          
    else:
        B=[]
    
    N_BASE_columns=[]
    for i in range(len(idx_N)):
        N_BASE_columns.append(A[:,idx_N[i]])
        
    if len(idx_N)>1:  
        N=N_BASE_columns[0].reshape(m,1)
        for i in range(1,len(idx_N)):
            N=np.hstack((N,N_BASE_columns[i].reshape(m,1)))
    elif len(idx_N)==1:
        N=N_BASE_columns[0]          
    else:
        N=[]
        
        
        
    nbr_aux= m-len(idx_B)#numero de var artificias
    
    
    if nbr_aux != 0:#se precisar do probelma artificial
        B,C_B,C_N,idx_B,idx_N,idx_artf=prob_artf(m,n,nbr_aux,lista_m,flag_m,B,idx_B,idx_N)
        R=0
        while R==0:
            R,Xb,B,N,C_B,C_N,idx_B,idx_N=custos_rel(B,N,C_B,C_N,idx_B,idx_N)
            
           # R,Xb,B,N,C_B,C_N,idx_B,idx_N=Z[0],Z[1],Z[2],Z[3],Z[4],Z[5],Z[6],Z[7]
           
        F=check_fun(Xb,C_B,C_N,idx_B,idx_N)
        if F==0:
            idx_idx_artf=[]
            for i in idx_artf:
                idx_idx_artf.append(idx_N.index(i))
            N=np.delete(N,idx_idx_artf,axis=1)
            for i in idx_artf:
                '''
                if i in idx_B:                   
                    idx_B.remove(i)   
                '''
                if i in idx_N:
                    idx_N.remove(i)                    
        
        else:
            
            return B,N,idx_B,idx_N,C_B,C_N,0
        
    
    C_B=[]#custo idx_B
    C_N=[]#custo nao idx_N
    for i in idx_B:
        C_B.append(c[i])
        
    for i in idx_N:    
        C_N.append(c[i])
    
    return B,N,idx_B,idx_N,C_B,C_N,1
#%%simplex
def simplex(m,n,c,b,A):
    A=(np.array(A)).reshape(m,n)
    c=(np.array(c)).reshape(len(c),1)
    b=(np.array(b)).reshape(m,1)
    B,N,idx_B,idx_N,C_B,C_N,fac=particao(A,c,m,n)
    if fac == 0:
        return print("Não há solução factível")
    R=0
    while R==0:
        R,Xb,B,N,C_B,C_N,idx_B,idx_N=custos_rel(B,N,C_B,C_N,idx_B,idx_N)
     #   R,Xb,B,N,C_B,C_N,idx_B,idx_N=Z[0],Z[1],Z[2],Z[3],Z[4],Z[5],Z[6],Z[7]
    if R==2:
        return print("Problema não tem solucao ́otima finita.")

    F=check_fun(Xb,C_B,C_N,idx_B,idx_N)
    #ajeitar a ordem da solucao basica
    X = np.zeros((n,1))
    for i in range(len(idx_B)):
        X[idx_B[i]]=Xb[i]
    
    return print("Solução ótima:\n",X,"\nCom função objetivo valendo:", F[0])
#%%problema degenerado sem vr artificial
print("Exemplo 1:\n")
c=[-1,-1,0,0,0]
m,n=3,5
A=[1,1,1,0,0,2,1,0,1,0,1,2,0,0,1]
b=[10,15,15]

simplex(m,n,c,b,A)
print('\n')
#%%problema sem vr artificial
print("Exemplo 2:\n")

c=[-3,-5,0,0,0]
A=[1,0,1,0,0,0,1,0,1,0,3,2,0,0,1]
b=[6,6,18]
m,n=3,5

simplex(m,n,c,b,A)
print('\n')
#%%problema com vr artificial
print("Exemplo 3:\n")

c=[-1,2,0,0]
A=[1,1,-1,0,-1,1,0,-1]
b=[2,1]
m,n=2,4

simplex(m,n,c,b,A)
print('\n')
#%%problema infactivel
print("Exemplo 4:\n")

c=[3,4,0,0]
A=[1,1,1,0,2,1,0,-1]
b=[1,4]
m,n=2,4

simplex(m,n,c,b,A)
print('\n')
#%%problema ilimitado
print("Exemplo 5:\n")

c=[-1,-1,0,0]
A=[1,-1,1,0,-1,1,0,1]
b=[4,4]
m,n=2,4

simplex(m,n,c,b,A)
print('\n')
#%%
print("Exemplo 6:\n")

c=[1,1,0,0,0,0,0]
A=[3,2,-1,0,0,0,0,1,2,0,-1,0,0,0,1,0,0,0,-1,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,1]
b=[24,12,2,15,15]
m,n=5,7

simplex(m,n,c,b,A)
print('\n')
#%%
#OBS: se houver erro, limpe as variáveis antes de rodar novo problema
