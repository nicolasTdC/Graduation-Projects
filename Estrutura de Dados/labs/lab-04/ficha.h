/*

  ficha.h - interface contendo lista ligada e operadores sobre essa lista
            para armazenamento de fichas bibliográficas do
            Laboratório 4 de MC202GH.

  Autores: Nicolas Toledo de Camargo RA242524

  MC202G+H - 2 semestre de 2023.
  
*/

#include <stdio.h>
#include <stdlib.h>

typedef struct no *p_no;

struct no {
  char *doi, **autor;
  int ano, n_autores, volume;
  p_no prox;
};

/*
   Função que recebe um ponteiro para um ponteiro do primeiro nó de uma lista
   encadeada de fichas e uma string que representa o DOI do artigo.
   A função devolve o ponteiro para o nó que contém o artigo com o DOI correspondente
   ou então NULL caso o mesmo não se encontre na lista.
*/
p_no busca_ficha(p_no primeiro, char *doi);

/*
   Função que recebe um ponteiro para o primeiro nó de uma lista
   encadeada de fichas e a imprime na saída padrão.
*/
void imprime_ficha(p_no primeiro);

/*
   Função que aloca na memória um novo nó do tipo ficha e devolve um ponteiro
   para ele.
*/
p_no cria_fichario();

/*
   Função que lê da entrada uma linha contendo os dados de um artigo
   devolve o ponteiro de um registro que armazena esses dados. A linha deve
   conter um string (DOI), seguido de um inteiro que especifica o número de
   autores, os sobrenomes dos autores (um ou mais strings, de acordo com o
   inteiro descrito anterioremente) e de dois inteiros (ano e volume,
   respectivamente), sendo que esses dados são separados entre si por um
   espaço.
*/
p_no le_ficha();

/*
   Função que recebe um ponteiro para o primeiro nó de uma lista
   encadeada de fichas e um ponteiro para um nó de artigo.
   A função insere então o nó do artigo no início da lista e devolve o ponteiro
   para o novo primeiro nó.
*/
p_no insere_ficha(p_no primeiro, p_no novo);

/*
   Função que recebe um ponteiro para o primeiro nó de uma lista
   encadeada de fichas e o string do DOI do artigo. Se existir um nó com
   o DOI então o mesmo é removido da lista e a função devolve o ponteiro para
   o novo primeiro nó; caso contrário ela devolve o ponteiro para o primeiro nó sem alterações.
*/
p_no remove_ficha(p_no primeiro, char *doi);

/*
   Função que recebe o primeiro nó de uma lista encadeada de fichas e libera a
   memória alocada por todos os nós.
*/
void destroi_fichas(p_no primeiro);

/*
   Fim do arquivo de interface.
*/
