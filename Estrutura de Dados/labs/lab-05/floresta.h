/*

  floresta.h - interface do TAD para manipulação de Binary Search Tree (BST) 
               e pilha, aplicados no contexto de um jogo em uma floresta de monstros.

  Autor: Nicolas Toledo de Camargo 

  RA: 242524

  MC202G+H - 2 semestre de 2023.

*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Estrutura de um nó na árvore de busca binária, representando cada monstro na floresta.
typedef struct NoArvore {
    int poder; // valor numérico que representa o poder de um monstro.
    struct NoArvore *esq, *dir; // ponteiros para subárvores esquerda e direita.
} NoArvore, *p_no_arvore;

// Estrutura de um nó na pilha, utilizado para armazenar os caminhos percorridos na floresta.
typedef struct NoPilha {
    int poder; // valor numérico que representa o poder de um monstro.
    struct NoPilha *prox; // ponteiro para o próximo elemento na pilha.
} NoPilha, *p_no_pilha;

/* Operações da Árvore de Busca Binária (BST) */

/*
   Cria uma nova árvore vazia.
   Retorna um ponteiro para a raiz da árvore.
 */
p_no_arvore cria_percursos();

/*
  Insere um novo monstro na árvore de monstros. A inserção é feita de forma a manter a
  propriedade de busca binária, baseando-se no poder do monstro.
  raiz: ponteiro para a raiz da árvore.
  poder: valor do poder do monstro a ser inserido.
  Retorna um ponteiro para a raiz da árvore atualizada.
 */
p_no_arvore insere_monstro(p_no_arvore raiz, int poder);

/*
  Realiza uma busca na árvore para determinar os caminhos possíveis que o personagem pode
  percorrer mantendo a vida acima de zero, levando em consideração o poder dos monstros.
  raiz: ponteiro para a raiz da árvore.
  vida_personagem: quantidade de vida restante do personagem.
 */
void busca_caminhos(p_no_arvore raiz, int vida_personagem);

/*
  Libera toda a memória alocada pelos nós da árvore.
  raiz: ponteiro para a raiz da árvore.
 */
void destroi_percursos(p_no_arvore raiz);

/* Operações da Pilha */

/*
  Cria uma nova pilha vazia, para armazenamento dos caminhos percorridos.
  Retorna um ponteiro para o topo da pilha.
 */
p_no_pilha cria_pilha();

/*
  Imprime o conteúdo atual da pilha, utilizado para depuração e visualização dos caminhos.
  topo: ponteiro para o topo da pilha.
 */
void imprime_pilha(p_no_pilha topo);

/*
  Insere um novo elemento no topo da pilha, representando um passo no caminho do personagem.
  topo: ponteiro para o topo da pilha.
  poder: valor do poder do monstro no caminho.
  Retorna um ponteiro para o novo topo da pilha.
 */
p_no_pilha insere_na_pilha(p_no_pilha topo, int poder);

/*
  Remove o elemento do topo da pilha, utilizado quando o personagem retrocede um passo.
  topo: ponteiro para o topo da pilha.
  poder: endereço de uma variável onde o poder do monstro removido será armazenado.
  Retorna um ponteiro para o novo topo da pilha.
 */
p_no_pilha remove_da_pilha(p_no_pilha topo, int *poder);

/*
  Libera toda a memória alocada pelos elementos da pilha.
  topo: ponteiro para o topo da pilha.
 */
void destroi_pilha(p_no_pilha topo);

/*
   Fim do arquivo de interface.
*/
