/*

  cliente.c - Aplicação principal para o gerenciamento de estoque de uma loja de elementos químicos,
              utilizando estruturas de dados 'árvore binária de busca', como parte do Laboratório de MC202.

  Autor: Nicolas Toledo de Camargo

  RA: 242524

  MC202G+H - 2º semestre de 2023.

*/

#include "gerenciador.h"

int main() {
  p_no RAIZ = NULL;
  char comando[9];
  
  while (fgets(comando, 9, stdin) != NULL){
    if ( comando[0] == 'C'){
      char* string_numero = malloc(( 3 + 1 + 1) *sizeof(char));
      int _ = 2;
      while ( comando[_] != ' ' ) {
        string_numero[_ - 2] = comando[_];
        _ ++;
      }
      string_numero[_ - 2] = '\0';
      int numero_atomico = atoi(string_numero);
      free(string_numero );

      _ ++;
      int __ = 0;
      char* elemento = malloc(( 2 + 1 + 1) *sizeof(char));
      while ( comando[_] != '\0' && comando[_] != '\n') {
        elemento[__] = comando[_];
        _ ++;
        __++;
      }
      elemento[__] = '\0';

      int tamanho_string = strlen(elemento);
      char ultimo_char = elemento[tamanho_string - 1];
      if ( ultimo_char == '\r' || ultimo_char == '\n'){
        elemento[tamanho_string - 1] = '\0';
      }
     
      RAIZ = inserir(RAIZ, numero_atomico, elemento);
      free(elemento);
    }
    else if ( comando[0] == 'V') {
      char* elemento = malloc(( 3 + 1) *sizeof(char));
      int _ = 2;
      int __ = 0;
      while ( comando[_] != '\0' && comando[_] != '\n') {
        elemento[__] = comando[_];
        _ ++;
        __++;
      }
      elemento[__] = '\0';

      int tamanho_string = strlen(elemento);
      char ultimo_char = elemento[tamanho_string - 1];
      if ( ultimo_char == '\r' || ultimo_char == '\n'){
        elemento[tamanho_string - 1] = '\0';
      }

      RAIZ = remover(RAIZ, elemento);
      free(elemento);
    }
    else if ( comando[0] == 'E') { 
      p_no MAXIMO = maximo(RAIZ);
      imprimir(RAIZ, MAXIMO);
    }
    else if ( comando[0] == 'I') {
      int tamanho_comando = strlen(comando);
      char* string_numero = malloc(( tamanho_comando - 5 + 1 + 1) *sizeof(char));
      int _ = 2;
      while ( comando[_] != ' ' ) {
        string_numero[_ - 2] = comando[_];
        _ ++;
      }
      string_numero[_ - 2] = '\0';
      int numero_atomico = atoi(string_numero);
      free(string_numero );
      p_no flag = buscar(RAIZ, numero_atomico);

      if ( flag != NULL) {
        printf( "Sim\n" );
      }
      else { 
        printf( "Nao\n" );
      }
    }
    else if ( comando[0] == 'M' ) {
      if ( comando[1] == 'I' ){
        printf( "%s\n", minimo(RAIZ)->simbolo);
      }
      else {
        printf( "%s\n", maximo(RAIZ)->simbolo);
      }
    }
  }

  destruir_arvore(RAIZ);
  return 0;
}   
