/*

  labirinto.h - Interface contendo tipo e operadores sobre esse tipo
                para solucionar labirintos no Trabalho de MC202GH.

  Autores: Nicolas Toledo de Camargo RA242524

  MC202GH - 2 semestre de 2023.

*/

#include <stdio.h>
#include <stdlib.h>

/* 
  Definindo um tipo, usando struct, para
  representar o labirinto.
*/
typedef struct
{
    char **matriz;
    int linhas, colunas;
    int saidaX, saidaY;   /* Coordenadas da saída do labirinto */
} labirinto;

/* Protótipos das funções do TAD labirinto */


/*
   Função que cria e retorna um novo labirinto.
   Recebe: Número de linhas e colunas do labirinto.
   Faz: Aloca dinamicamente um labirinto com o número especificado de linhas e colunas.
   Retorna: Um ponteiro para o labirinto alocado.
*/
labirinto* criar_labirinto(int linhas, int colunas);

/*
    Função que lê o conteúdo do labirinto da entrada padrão.
    Recebe: Um ponteiro para o labirinto.
    Faz: Preenche a matriz do labirinto lendo os caracteres da entrada padrão.
    Retorna: Nada.
*/
void ler_labirinto(labirinto *l);

/*
   Função que libera a memória ocupada por um labirinto.
   Recebe: Um ponteiro para o labirinto.
   Faz: Libera a memória ocupada por todas as linhas da matriz e pela própria matriz.
   Retorna: Nada.
*/
void destruir_labirinto(labirinto *l);

/*
   Função auxiliar recursiva que busca uma saída no labirinto.
   Recebe: Uma matriz de caracteres, as dimensões da matriz e as coordenadas atuais da busca.
   Faz: Verifica se a posição atual é válida e tenta encontrar uma saída movendo-se em diferentes direções.
   Retorna: 1 se uma saída foi encontrada, 0 caso contrário.
*/
int buscar_saida_recursivamente(char **matriz, int linhas, int colunas, int x_atual, int y_atual); 

/*
    Função que busca a saída do labirinto a partir de um ponto inicial.
    Recebe: Um ponteiro para o labirinto e as coordenadas iniciais para começar a busca.
    Faz: Usa a função auxiliar "buscar_saida_recursivamente" para tentar encontrar um caminho da posição inicial até a saída. 
    Retorna: Um novo labirinto que representa o caminho encontrado.
*/
labirinto* buscar_saida(labirinto *l, int x, int y);


/*
   Função que imprime o conteúdo do labirinto no console.
   Recebe: Um ponteiro para o labirinto.
   Faz: Itera sobre a matriz e imprime cada caracter.
   Retorna: Nada.

*/
void imprimir_labirinto(labirinto *l);


/*
   Fim do arquivo de interface.
*/
