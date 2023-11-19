/*

  cliente.c - Implementação dos operadores para manipulação de fichas de
              referências bibliográficas do Laboratório 2 de MC202G+H.

  Autor: Nicolas Toledo de Camargo RA 242524

  MC202G+H - 2 semestre de 2023.

*/

#include "ficha.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX 1000

ficha * le_ficha(){
  ficha * new_ficha = malloc(sizeof(ficha));
  char *input_ficha = malloc(MAX*sizeof(char));
  int i = 0;
  while (1) {
    int ch = getchar();

    if (ch == '\n' || ch == EOF) {
      break;
    }

    if (i < MAX - 1) { 
      input_ficha[i] = (char) ch;
      i++;
    }

  }
  input_ficha[i] = '\0';
  int indice_letra=0;
  int tamanho_doi =0;
  int numero_autores;
  char * ponteiro_ano;
  char * ponteiro_volume;
  char * ponteiro_numero_autores;
  int numero_letras_nome = 0;
  for (int contador_espacos = 0; contador_espacos<5;contador_espacos++){
    if ( contador_espacos == 0){
      while ( input_ficha[indice_letra] != ' ' ) {
        tamanho_doi++;
        indice_letra++;
      }
      indice_letra++;
      new_ficha->doi = malloc((tamanho_doi+ 1)*sizeof(char));
      for ( int _ =0; _<tamanho_doi; _++) {
        (new_ficha->doi)[_]= input_ficha[_];
      }
      (new_ficha->doi)[tamanho_doi] = '\0';
    }

    else if ( contador_espacos == 1 ){

      int numero_digitos_autores =0;
      while ( input_ficha[indice_letra] != ' ' ) {
        numero_digitos_autores++;
        indice_letra++;
      }
      indice_letra++;
      ponteiro_numero_autores = malloc((numero_digitos_autores+1)*sizeof(char));
      for ( int _ =0; _<numero_digitos_autores; _++) {
        ponteiro_numero_autores[_]= input_ficha[indice_letra-numero_digitos_autores+_-1];
      }
      ponteiro_numero_autores[numero_digitos_autores]='\0';
      numero_autores = atoi(ponteiro_numero_autores);
      new_ficha->n_autores= numero_autores;
      free(ponteiro_numero_autores);
    }

    else if ( contador_espacos == 2 ) { 
      new_ficha->autor = malloc((numero_autores)*sizeof(char *) );
      for (int contador_autores = 0; contador_autores<numero_autores; contador_autores++){
        numero_letras_nome = 0;
        while ( input_ficha[indice_letra] != ' ' ) {
          numero_letras_nome++;
          indice_letra++;
        }
        indice_letra++;
        (new_ficha->autor)[contador_autores] = malloc((numero_letras_nome+1)*sizeof(char));
        for ( int _ =0; _<numero_letras_nome; _++) {
          (new_ficha->autor)[contador_autores][_]= input_ficha[indice_letra-numero_letras_nome+_-1];
        }
        (new_ficha->autor)[contador_autores][numero_letras_nome] = '\0';
      }

    }
    else if ( contador_espacos == 3 ) {
      int numero_digitos_ano =0;
      while ( input_ficha[indice_letra] != ' ' ) {
        numero_digitos_ano++;
        indice_letra++;
      }
      indice_letra++;
      ponteiro_ano = malloc((numero_digitos_ano+1)*sizeof(char));
      char digito_ano;
      for ( int _ =0; _<numero_digitos_ano; _++) {
          digito_ano = input_ficha[indice_letra-numero_digitos_ano+_-1];
          ponteiro_ano[_]= digito_ano;
      }
      ponteiro_ano[numero_digitos_ano]='\0';
      new_ficha->ano= (atoi(ponteiro_ano));
      free(ponteiro_ano);
    }

    else if ( contador_espacos == 4 ) {
      int numero_digitos_volume =0;
      while ( input_ficha[indice_letra] != '\0' && input_ficha[indice_letra] != '\n') {
        numero_digitos_volume++;
        indice_letra++;
      }
      indice_letra++;
      ponteiro_volume = malloc((numero_digitos_volume+1)*sizeof(char));
      for ( int _ =0; _<numero_digitos_volume; _++) {
          ponteiro_volume[_]= input_ficha[indice_letra-numero_digitos_volume+_-1];
      }
      ponteiro_volume[numero_digitos_volume] = '\0';
      new_ficha->volume= (atoi(ponteiro_volume));
      free(ponteiro_volume);
    }
  }
  free(input_ficha);
  return new_ficha;
}

void destroi_ficha(ficha * ptr_artigo){

  if (ptr_artigo->autor != NULL) {
    for ( int numero_autores = 0 ; numero_autores< ptr_artigo->n_autores;numero_autores++){
      free((ptr_artigo->autor)[numero_autores]);
    }
    free(ptr_artigo->autor);
    free(ptr_artigo->doi);
  }
  free(ptr_artigo);

  return;
}

ficha ** cria_fichario (int n){
  ficha ** fichario = malloc(n*sizeof(ficha *));
  for (int i=0 ; i < n; i++){
    fichario[i] = malloc(sizeof(ficha)); 
    fichario[i]->doi = NULL;
    fichario[i]->autor = NULL;
  }
  return fichario;
}

void imprime_ficha(ficha * ptr_artigo){
  if (ptr_artigo->n_autores>3){
    printf("%s %s, %s, %s, et al. (%d) %d\n",ptr_artigo->doi, ptr_artigo->autor[0], ptr_artigo->autor[1],
          ptr_artigo->autor[2], ptr_artigo->ano,ptr_artigo->volume);
    return;
  }
  else if (ptr_artigo->n_autores==3){
    printf("%s %s, %s, %s (%d) %d\n",ptr_artigo->doi, ptr_artigo->autor[0], ptr_artigo->autor[1],
          ptr_artigo->autor[2], ptr_artigo->ano,ptr_artigo->volume);
    return;
  }
  else if (ptr_artigo->n_autores==2){
    printf("%s %s, %s (%d) %d\n",ptr_artigo->doi, ptr_artigo->autor[0], ptr_artigo->autor[1],
          ptr_artigo->ano,ptr_artigo->volume);
    return;
  }
  printf("%s %s (%d) %d\n",ptr_artigo->doi, ptr_artigo->autor[0],
        ptr_artigo->ano,ptr_artigo->volume);
  return;
}

int insere_ficha (ficha ** ptr_vetor, int n, ficha * ptr_artigo){
  for (int _ = 0 ; _<n;_++){
    if ( (ptr_vetor[_])->doi == NULL){

      destroi_ficha((ptr_vetor[_]));
     // ptr_vetor[_] = malloc(sizeof(ficha));
      ptr_vetor[_] = ptr_artigo;
      return 1;
    }
  }
  printf("Erro ao inserir DOI %s\n",ptr_artigo->doi);
  destroi_ficha(ptr_artigo);
  return 0;
}

int busca_ficha (ficha ** ptr_vetor, int n, char * doi){
  for (int _ = 0; _ < n; _ ++){
    if (  (ptr_vetor[_])->doi  == NULL){
      continue;
    }
    char teste;
    char teste2;
    int flag_string_igual=strlen( (ptr_vetor[_])->doi );
    int tam_doi = strlen(doi);
    for (int i = 0; ( (ptr_vetor[_])->doi )[i] != '\0'; i++) {
      if ( i > tam_doi ){
        if ( flag_string_igual == 0){
          return _;
        }
        continue;
      }
      teste = ((ptr_vetor[_])->doi )[i];
      teste2 = doi[i];
      if (teste == teste2){
        flag_string_igual--;
      }
      if ( flag_string_igual == 0){
        return _;
      }
    }
  }
  return -1;
}

int remove_ficha(ficha ** ptr_vetor, int n, char * doi){
  int flag = busca_ficha (ptr_vetor,n,doi);
  if ( flag == -1 ){
   // printf("DOI %s inexistente\n", doi);
    printf("DOI %.*s inexistente\n", (int)strlen(doi) -1, doi);
    return 0;
  }
  
 // printf("DOI %s removido\n", doi);
  printf("DOI %.*s removido\n", (int)strlen(doi) -1, doi);

  destroi_ficha(ptr_vetor[flag]);

  ptr_vetor[flag] = malloc(sizeof(ficha)); 
  ptr_vetor[flag]->doi = NULL;

  ptr_vetor[flag]->autor = NULL;

  return 1;
}