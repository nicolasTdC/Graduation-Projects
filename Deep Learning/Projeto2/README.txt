Instruções:

1. Extraia o conteúdo deste arquivo zip.

2. Abra o notebook do projeto (arquivo "main.ipynb").

3. Execute a célula "# Importação de dados". Caso ocorra algum erro, certifique-se de que a localização dos arquivos está correta e que todas as bibliotecas necessárias estão instaladas.

4. Na célula "# Tratamento de Dados", certifique-se de que as variáveis n_pre e n_pos estão definidas de acordo com o número de unidades de pré-ativação e de pós-ativação do modelo que se deseja treinar ou testar, e então execute essa célula.

5. A célula "# Treinamento do Modelo" somente deve ser executada caso se deseje treinar um modelo do zero. Neste caso, selecione o número de épocas alterando o valor da variável epocas, e o tamanho do conjunto de treino extraído do dataset alterando o valor da variável m. Execute a célula e o treinamento será iniciado. Durante o treinamento, é possível acompanhar qual é a época atual, bem como o tempo gasto nas épocas anteriores. Esteja ciente de que quanto maior o número de épocas e de unidades de ativação, maior será o tempo gasto no treinamento. O modelo treinado será salvo na pasta models, com o nome na forma "model_{epocas}-epocas_{n_pre}-preativacoes_{n_pos}-posativacoes.h5". Caso já exista outro modelo com o mesmo nome, ele será sobrescrito.

6. A célula "# Testes do Modelo" somente deve ser executada caso se deseje testar o modelo. Neste caso, certifique-se de atualizar nesta célula o valor da variável m, caso esteja desatualizado, pois a partir dele será definido o conjunto de teste, e escolha o arquivo que será testado alterando o nome do arquivo na função modelo.load_weights('models/model_{epocas}-epocas_{n_pre}-preativacoes_{n_pos}-posativacoes.h5'). Execute a célula e será exibido como output o valor predito e o valor esperado para cada exemplo do conjunto de teste, e por fim será exibida a acurácia do modelo. Caso ocorra algum erro, certifique-se de que o modelo que se deseja testar possui o mesmo número de unidades de pré-ativação e de pós-ativação que estão definidos na célula "# Tratamento de Dados", e reinicie o processo.

6. A célula "# Mapa de Atenção" permite realizar testes adicionais com um exemplo de sua escolha, alterando o valor da variável exemplo. Execute a célula e será exibido como output o mapa de atenção do exemplo escolhido.