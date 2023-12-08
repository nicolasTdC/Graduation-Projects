import implementacao as imp
import random
import numpy as np
import matplotlib.pyplot as plt
import os
import time
import pandas as pd

output_folder = 'imagens'
os.makedirs(output_folder, exist_ok=True)

# Funções, metodos e hiperparametros
funcoes_nomes = [ 'quadrática', 'de Rosenbrook', "de Styblinsky-Tang", 'de Rastringin' ]
funcoes = [ 'quadratica', 'rosenbrook', 'styblinsk_tang', 'rastringin' ]

hiperpar_grid = [4, 2, 3.9, 4]  # tamanho grid considerada
hiperpar_start_curva = [0, 0, -160, -20]  # start da curvas
hiperpar_stop_curva = [50, 36, 20, 60] # stop da curvas
hiperpar_step_curva = [2, 2, 10, 10] # step das curvas

metodos_nomes = [ 'do gradiente', 'de Newton', 'CP1', 'DFP']
metodos = [ 'metodo_gradiente', 'metodo_newton', 'metodo_secante_c_posto1', 'metodo_secante_DFP']

n_teste = [ 2 , 6, 10 ]

epsilon_teste = [ 1e-6, 1e-2, 1]

hiperpar_perto = 1 # desvio padrao que gera ponto perto
hiperpar_longe = 100 # desvio padrao que gera ponto longe

numero_pontos = 5 # numero de pontos perto/longe

M = 300 # numero maximo iteracoes

ver_todos_resultados = False # True se qusier ver o resultado de todos os pontos

# Dicionario para guardar resultados
results_dict = {}

initials = ['Perto', 'Longe']
for func in funcoes_nomes:
    func_dict = {}
    
    for n in n_teste:
        n_dict = {}
        for eps in epsilon_teste:
            eps_dict = {}
            for method in metodos_nomes:
                method_dict = {}
                for init_point in initials:
                    method_dict[init_point] = {'error': 0, 'time': 0, 'epochs': 0}
                
                eps_dict[method] = method_dict
            
            n_dict[str(eps)] = eps_dict
        
        func_dict[str(n)] = n_dict
    
    results_dict[func] = func_dict    

plot_counter = 1

# Para cada funcao, para cada n, para cada epsilon, para cada metodo, testa os pontos iniciais
for funcao in funcoes_nomes[:]:
    
    contador_funcao =  funcoes_nomes.index(funcao)
    
    print(f'Testes para função {funcao}:\n')

    for n in n_teste[:]: 
        if funcao ==  'quadrática' or funcao ==  'de Rastringin':
            min_global = np.zeros(n)
        elif funcao ==  'de Rosenbrook':
            min_global = np.ones(n)
        elif funcao ==  'de Styblinsky-Tang':
            min_global = np.array( [-2.9035 for _ in range(n) ] )

        print('    Teste para n =', n,' :\n') 
        
        minimo_global = np.round(getattr(imp, funcoes[contador_funcao])(min_global), 4)
        
        if n == 2:
            print('        Min global em:', min_global,', com função valendo: ', minimo_global, '\n')

        else:
            print('        Min global com função valendo: ', minimo_global, '\n')
        x0_teste = [[],[]]

        for _ in range (numero_pontos) :
            x0_teste[0].append([ random.gauss(min_global[0], hiperpar_perto) for _ in range(n) ]) # perto do global
            x0_teste[1].append([ random.gauss(min_global[0], hiperpar_longe) for _ in range(n) ]) # longe do global

        x0_teste = np.array(x0_teste)    
        for epsilon in epsilon_teste[:]: 
          print('        Teste para epsilon =', epsilon,' :\n')    
            
          contador_metodo = 0  
          for metodo in metodos_nomes[:]: 
              
              if n == 2:
                  if funcao != "de Styblinsky-Tang" :
                      x = np.linspace(min_global[0] - hiperpar_grid[contador_funcao],
                                      min_global[0] + hiperpar_grid[contador_funcao] , 400)
                      y = np.linspace(min_global[0] - hiperpar_grid[contador_funcao],
                                      min_global[0] + hiperpar_grid[contador_funcao], 400)

                  else:
                      x = np.linspace(0 - hiperpar_grid[contador_funcao],
                                      0 + hiperpar_grid[contador_funcao] , 400)
                      y = np.linspace(0 - hiperpar_grid[contador_funcao],
                                     0 + hiperpar_grid[contador_funcao], 400)
                    
                  X, Y = np.meshgrid(x, y)

                  Z = np.zeros_like(X)
                  for i in range(X.shape[0]):
                      for j in range(X.shape[1]):
                          Z[i, j] = getattr(imp,funcoes[contador_funcao])([X[i, j], Y[i, j]])
                  plt.figure(plot_counter)
                  plot_counter+=1
                  contour = plt.contourf(X, Y, Z,
                                         levels=np.arange(hiperpar_start_curva[contador_funcao],
                                                          hiperpar_stop_curva[contador_funcao],
                                                          hiperpar_step_curva[contador_funcao]),
                                                          cmap='cividis')
                  contour2 = plt.contour(X, Y, Z,
                                         levels=np.arange(hiperpar_start_curva[contador_funcao],
                                                          hiperpar_stop_curva[contador_funcao],
                                                          hiperpar_step_curva[contador_funcao]),
                                                          cmap='Greys_r', alpha = 0.2)
                  if funcao == 'de Rosenbrook':
                      contour3 = plt.contour(X, Y, Z,
                                             levels=np.arange(hiperpar_start_curva[contador_funcao],
                                                              2000,
                                                              50),
                                                              cmap='Greys_r', alpha = 0.3)
            
                  plt.scatter(min_global[0], min_global[1], color = 'green' , label = 'Minimizador global', s = 75)
                  cbar = plt.colorbar(contour)
                  cores = ['red', 'deepskyblue', 'black']

              print(f'            Método {metodo}:\n')

              marker = [ '^', 'x', 's']
              flag_label = 0
              flag_label2 = 0
              erro_perto = 0
              tempo_perto = 0
              media_iteracoes = 0
              
              for ponto_perto in x0_teste[0]:
                  if n == 2:
                      if ponto_perto[0] < x[-1] and ponto_perto[1] < y[-1] and ponto_perto[0] > x[0] and ponto_perto[1] > x[0]:
                          if flag_label2 == 0:
                              plt.scatter(ponto_perto[0], ponto_perto[1], color = cores[2] ,
                                          label = 'Ponto inicial',marker=marker[2],
                                          s = 50)
                              flag_label2 = 1
                          else:
                               plt.scatter(ponto_perto[0], ponto_perto[1], color = cores[2] ,
                                           marker=marker[2],
                                           s = 50)
                  
                  start = time.time()
                  res = getattr(imp, metodos[contador_metodo])(ponto_perto, getattr(imp,funcoes[contador_funcao] ), epsilon, M= M)
                  end = time.time()
                  tempo_perto += end - start
                  
                  ponto_res = res[0]
                  iteracoes = res[1]

                  minimo_local = np.round(getattr(imp, funcoes[contador_funcao])(ponto_res), 4)
                  
                  erro_perto += abs(minimo_local - minimo_global)
                  media_iteracoes+=  iteracoes                 
                  if n == 2:
                      
                      if ver_todos_resultados == True:

                          print('                Teste para vetor inicial ', np.round(ponto_perto, 4),' :\n')    
                          print('                    Min local em:', np.round(ponto_res, 4),f', após {iteracoes} iterações' ,
                                ', e com função valendo:',
                                minimo_local, '\n')
                      if ponto_res[0] < x[-1] and ponto_res[1] < y[-1] and ponto_res[0] > x[0] and ponto_res[1] > x[0]:
                          if flag_label == 0:
    
    
                              plt.scatter(ponto_res[0], ponto_res[1], color = cores[0] ,
                                          label = f'Minimizador local para ponto inicial {initials[0]}',marker=marker[0],
                                          s = 50)
                              flag_label = 1
    
                          else:
                              plt.scatter(ponto_res[0], ponto_res[1], color = cores[0] ,
                                          marker=marker[0],
                                          s = 50)

                  else:
                      if ver_todos_resultados == True:

                          print(f'                Teste para vetor inicial {initials[0]} do minimizador global: ','\n') 
                          print('                    Min local com função valendo:',
                                minimo_local, f', após {iteracoes} iterações\n')
              media_iteracoes = media_iteracoes/numero_pontos
              erro_perto_medio = erro_perto/numero_pontos
              tempo_perto_medio = tempo_perto/numero_pontos
              
              print('                Erro médio para ponto perto: ',np.round(erro_perto_medio, 4),'\n') 
              print('                Tempo médio para ponto perto: ',np.round(tempo_perto_medio, 4),'\n') 
              print('                Média de iterações para ponto perto: ',np.round( media_iteracoes ),'\n') 
              results_dict[funcao][str(n)][str(epsilon)][metodo][initials[0]]['error'] = np.round(erro_perto_medio, 4)
              results_dict[funcao][str(n)][str(epsilon)][metodo][initials[0]]['time'] = np.round(tempo_perto_medio, 4)
              results_dict[funcao][str(n)][str(epsilon)][metodo][initials[0]]['epochs'] = np.round(media_iteracoes)

              flag_label = 0  
              flag_label2 = 0    

              erro_longe = 0
              tempo_longe = 0
              media_iteracoes = 0

              for ponto_longe in x0_teste[1]:  
                  
                  if n == 2:

                      if ponto_longe[0] < x[-1] and ponto_longe[1] < y[-1] and ponto_longe[0] > x[0] and ponto_longe[1] > x[0]:
                          if flag_label2 == 0:
                              plt.scatter(ponto_longe[0], ponto_longe[1], color = cores[2] ,
                                          label = 'Ponto inicial',marker=marker[2],
                                          s = 75)
                          else:
                              plt.scatter(ponto_longe[0], ponto_longe[1], color = cores[2] ,
                                          marker=marker[2],
                                          s = 75)
                                           
                  start = time.time()

                  res = getattr(imp, metodos[contador_metodo])(ponto_longe, getattr(imp,funcoes[contador_funcao] ),
                                                                     epsilon, M= M)
                  end = time.time()
                  tempo_longe += end - start
                  
                  ponto_res = res[0]
                  
                  iteracoes = res[1]
                  
                  minimo_local = np.round(getattr(imp, funcoes[contador_funcao])(ponto_res), 4)

                  erro_longe += abs(minimo_local - minimo_global)
                  media_iteracoes+=iteracoes
                  if n == 2:
                      if ponto_res[0] < x[-1] and ponto_res[1] < y[-1] and ponto_res[0] > x[0] and ponto_res[1] > x[0]:
                          if ver_todos_resultados == True:

                              print('                Teste para vetor inicial ', np.round(ponto_longe, 4),' :\n')    
                              print('                    Min local em:', np.round(ponto_res, 4),f', após {iteracoes} iterações' , ', e com função valendo:',
                                    minimo_local, '\n')

                              
                          if flag_label == 0:
                              plt.scatter(ponto_res[0], ponto_res[1], color = cores[1] ,
                                          label = f'Minimizador local para ponto inicial {initials[1]}',marker=marker[1],
                                          s = 75)
                              flag_label = 1    
                          else:
                               plt.scatter(ponto_res[0], ponto_res[1], color = cores[1] ,
                                          marker=marker[1],
                                           s = 75)                 

                  else:
                      if ver_todos_resultados == True:

                          print(f'                Teste para vetor inicial {initials[1]} do minimizador global: ','\n') 
                          print('                    Min local com função valendo:',
                                minimo_local, f', após {iteracoes} iterações\n')  
              media_iteracoes = media_iteracoes/numero_pontos
            
              erro_longe_medio = erro_longe/numero_pontos
              tempo_longe_medio = tempo_longe/numero_pontos
              
              print('                Erro médio para ponto longe: ',np.round(erro_longe_medio, 4),'\n') 
              print('                Tempo médio para ponto longe: ',np.round(tempo_longe_medio,4),'\n')         
              print('                Média de iterações para ponto longe: ',np.round( media_iteracoes ),'\n')  
              results_dict[funcao][str(n)][str(epsilon)][metodo][initials[1]]['error'] = np.round(erro_longe_medio, 4)
              results_dict[funcao][str(n)][str(epsilon)][metodo][initials[1]]['time'] = np.round(tempo_longe_medio, 4)
              results_dict[funcao][str(n)][str(epsilon)][metodo][initials[1]]['epochs'] = np.round(media_iteracoes)

              if n ==2:
                  plt.xlabel('x')
                  plt.ylabel('y')
                  plt.title(f'Função {funcao} | Método {metodo} | Epsilon {epsilon}')
                  legend = plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), title='Legenda',
                                      prop={'size': 7})
                  plt.subplots_adjust(bottom=0.2)

                  plt.grid(False)
                  nome_do_arquivo = f'{funcao}_{metodo}_{epsilon}.png'
                  caminho_completo = os.path.join(output_folder, nome_do_arquivo)
                  plt.savefig(caminho_completo, bbox_inches='tight')
                  plt.show(block=False) 
                  plt.pause(0.1)
                  
              contador_metodo+=1
plt.show()  

# Mostra resultados
flat_results = []

for func_name, n_dict in results_dict.items():
    for n, eps_dict in n_dict.items():
        for eps, method_dict in eps_dict.items():
            for method, init_dict in method_dict.items():
                for init_point, values in init_dict.items():
                    flat_results.append({
                        'Função': func_name,
                        'n': n,
                        'Epsilon': eps,
                        'Método': method,
                        'Ponto inicial': init_point,
                        'Erro': values['error'],
                        'Tempo': values['time'],
                        'Épocas': values['epochs']
                    })

df = pd.DataFrame(flat_results)

pivot_df = df.pivot_table(index=['Função', 'n', 'Epsilon', 'Método', 'Ponto inicial'],
                          values=['Erro', 'Tempo', 'Épocas'],
                          aggfunc='first')

save_path = 'tabelas'

for idx, group_df in pivot_df.groupby(['Função', 'n', 'Epsilon']):
    print(f"\nFunção: {idx[0]}, n: {idx[1]}, Epsilon: {idx[2]}\n")
    df_editada = group_df.reset_index().drop(['Função', 'n', 'Epsilon'], axis=1).iloc[::-1]
    file_path = os.path.join(save_path, f"{idx[0]}_{idx[1]}_{idx[2]}.csv")
    
    df_editada.to_csv(file_path, index=False)
    print(df_editada.to_string(index=False))
    fig, ax = plt.subplots(figsize=(8, 2))  
    ax.axis('off')  
    table = ax.table(cellText=df_editada.values,
                     colLabels=df_editada.columns,
                     cellLoc='center',
                     loc='center')
    file_path = os.path.join(save_path, f"{idx[0]}_{idx[1]}_{idx[2]}.png")

    plt.savefig(file_path, bbox_inches='tight')
    plt.close()  
    
