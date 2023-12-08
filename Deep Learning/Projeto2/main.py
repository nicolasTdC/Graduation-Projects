# MS960 - Aprendizado de Máquinas: Aspectos Teóricos e Práticos
# Projeto 2 - Tradução Automática Usando Atenção

import pickle
from implementacao import *

#%% Importação dos dados:

import pickle
from implementacao import *

dataset_path = "files/dataset.pkl"
with open(dataset_path, 'rb') as file:
  dataset = pickle.load(file)

human_vocab_path = "files/human_vocab.pkl"
with open(human_vocab_path, 'rb') as file:
  human_vocab = pickle.load(file)

machine_vocab_path = "files/machine_vocab.pkl"
with open(machine_vocab_path, 'rb') as file:
  machine_vocab = pickle.load(file)

inv_machine_vocab_path = "files/inv_machine_vocab.pkl"
with open(inv_machine_vocab_path, 'rb') as file:
  inv_machine_vocab = pickle.load(file)

#%% Tratamento dos dados:

Tx = 30 # Tamanho max da entrada (exemplo de entrada do dataset com 26 caracteres: "wednesday february 11 1970")
Ty = 10 # Tamanho max de saída (4 caracteres para o ano + 2 para o mês + 2 para o dia + 2 para os separadores: "YYYY-MM-DD")

Xoh, Yoh = converter_para_one_hot(Tx, Ty, dataset, machine_vocab, human_vocab) # Converte os caracteres para One Hot Vectors

#%% Camadas compartilhadas por todos os passos temporais no mecanismo de atenção:

n_pre = 32 # Número de unidades de pré-ativação
n_pos = 64 # Número de unidades de pós-ativação

ferramentas_compartilhadas = ferramentas_atencao(Tx, n_pos, machine_vocab)

#%% Modelo:

modelo = modelo(Tx, Ty, n_pre, n_pos, len(human_vocab), len(machine_vocab),
                ferramentas_compartilhadas)

modelo.compile(optimizer='Adam',
               loss='categorical_crossentropy',
               metrics=['accuracy'])

#%% Treinamento do modelo:

epocas = 50 # Número de épocas

m = round(len(dataset) * 0.99) # Número de exemplos para este treino

treinamento(Xoh, Yoh, modelo, m, n_pos, n_pre, epocas) # Salva os pesos deste treino

#%% Testes do modelo:

modelo.load_weights('models/model.h5') # Carregar modelo treinado para ser testado

m = round(len(dataset) * 0.99) # Novamente a variável m, caso a célula de treinamento não tenha sido executada

m2 = len(dataset) - m # Número de exemplos para teste

dataset_teste = dataset[len(dataset) - m2:]

testes(dataset_teste, n_pos, Tx, human_vocab, inv_machine_vocab, modelo)

#%% Mapa de atenção:

exemplo = '25.12.2990'

mapa = plot_attention_map(modelo,
                          human_vocab,
                          inv_machine_vocab,
                          exemplo,
                          n_pos=n_pos)
