/*

  ficha.h - interface contendo tipo e operadores sobre esse tipo
            para armazenamento de fichas bibliográficas do
            Laboratório 2 de MC202GH.

 Autor: Nicolas Toledo de Camargo RA 242524

  MC202G+H - 2 semestre de 2023.

*/

#include <stdio.h>
#include <stdlib.h>

/*
  Definindo um tipo, usando struct, para
  armazenar fichas bibliográficas.
*/
typedef struct
{
  char * doi, ** autor;
  int ano, n_autores, volume;
} ficha;


/*
   Função que recebe um ponteiro para um vetor de fichas, um inteiro n que
   diz o tamanho do vetor e uma string que representa o DOI do artigo.
   A função devolve o índice do artigo no vetor de fichas ou então
   -1 caso o mesmo não se encontre no vetor.
*/
int busca_ficha (ficha ** ptr_vetor, int n, char * doi);


/*
   Função que recebe um inteiro positivo n, aloca na memória um vetor do tipo
   ficha com n registros vazios (i.e., registro com DOI setado com string
   vazio) e devolve um ponteiro para a primeira posição desse vetor.
*/
ficha ** cria_fichario (int n);


/*
   Função que recebe um ponteiro de um registro contendo a ficha de um
   artigo e a imprime na saída padrão.
*/
void imprime_ficha(ficha * ptr_artigo);


/*
   Função que recebe um ponteiro para o endereço do ponteiro de um vetor de
   fichas, um ponteiro para um inteiro n que diz o tamanho do vetor e um
   ponteiro para uma ficha de artigo.
   A função insere então os dados do artigo no primeiro índice disponível
   (i.e., com DOI vazio) e devolve 1; caso não exista índice disponível a função
   devolve zero.
*/
int insere_ficha (ficha ** ptr_vetor, int n, ficha * ptr_artigo);


/*
   Função que lê da entrada uma linha contendo os dados de um artigo
   devolve o ponteiro de um registro que armazena esses dados. A linha deve
   conter um string (DOI), seguido de um inteiro que especifica o número de
   autores, os sobrenomes dos autores (um ou mais strings, de acordo com o
   inteiro descrito anterioremente) e de dois inteiros (ano e volume,
   respectivamente), sendo que esses dados são separados entre si por um
   espaço.
*/
ficha * le_ficha();


/*
   Função que recebe um ponteiro para um vetor de fichas, um inteiro n que diz
   o tamanho do vetor e o string do DOI do artigo. Se existir um registro com
   o DOI então o mesmo é setado como string vazio e a função devolve 1; caso
   contrário ela devolve 0.
*/
int remove_ficha (ficha ** ptr_vetor, int n, char * doi);


/*
   Função que recebe um ponteiro de um registro contendo a ficha de um
   artigo e a libera a memória alocada por ela
*/
void destroi_ficha(ficha * ptr_artigo);

/*
   Fim do arquivo de interface.
*/
