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

p_no le_ficha(){
  p_no new_ficha = malloc(sizeof(struct no));
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
  new_ficha->prox = NULL;
  free(input_ficha);
  return new_ficha;
}

void destroi_fichas(p_no primeiro){
  p_no anterior = NULL;
  p_no atual = primeiro;
  while (atual->prox!=NULL){
    anterior = atual;
    atual = atual->prox;
  }
  if (atual != primeiro){
    for ( int numero_autores = 0 ; numero_autores< atual->n_autores;numero_autores++){
      free((atual->autor)[numero_autores]);
    }
    free(atual->autor);
    free(atual->doi);
    free(atual);
    anterior->prox  = NULL;
    destroi_fichas(primeiro);
  }

  else{
    for ( int numero_autores = 0 ; numero_autores< atual->n_autores;numero_autores++){
      free((atual->autor)[numero_autores]);
    }
    free(atual->autor);
    free(atual->doi);
    free(atual);
  }
}

p_no cria_fichario(){
  p_no fichario = malloc(sizeof(struct no));
  fichario->doi = NULL;
  fichario->autor = NULL;
  fichario->prox = NULL;
  return fichario;
}

void imprime_ficha(p_no primeiro){
  p_no atual = primeiro;
  while(atual != NULL) {
    if (atual->n_autores>3){
      printf("%s %s, %s, %s, et al. (%d) %d\n",atual->doi, atual->autor[0], atual->autor[1],
            atual->autor[2], atual->ano,atual->volume);
    }
    else if (atual->n_autores==3){
      printf("%s %s, %s, %s (%d) %d\n",atual->doi, atual->autor[0], atual->autor[1],
            atual->autor[2], atual->ano,atual->volume);
    }
    else if (atual->n_autores==2){
      printf("%s %s, %s (%d) %d\n",atual->doi, atual->autor[0], atual->autor[1],
            atual->ano,atual->volume);
    }
    else {
      printf("%s %s (%d) %d\n",atual->doi, atual->autor[0],
          atual->ano,atual->volume);
    }
    atual = atual->prox;
  };
}

p_no insere_ficha(p_no primeiro, p_no novo){
  novo->prox = primeiro;
  return novo;
}

p_no busca_ficha(p_no primeiro, char *doi){
  p_no atual = primeiro;
  do {
    char teste;
    char teste2;
    int flag_string_igual=strlen( atual->doi );
    int tam_doi = strlen(doi);
    for (int i = 0; ( atual->doi )[i] != '\0'; i++) {
      if ( i > tam_doi ){
        if ( flag_string_igual == 0){
          return atual;
        }
        continue;
      }
      teste = (atual->doi )[i];
      teste2 = doi[i];
      if (teste == teste2){
        flag_string_igual--;
      }
      if ( flag_string_igual == 0){
        return atual;
      }
    }
    atual = atual->prox;
  } while(atual != NULL);
  return NULL;
}

p_no remove_ficha(p_no primeiro, char *doi){
  p_no flag = busca_ficha (primeiro,doi);
  if ( flag == NULL ){
    doi[strcspn(doi, "\n")] = '\0';
    doi[strcspn(doi, "\r")] = '\0';
    printf("DOI %s inexistente\n", doi);
    return primeiro;
  }
  doi[strcspn(doi, "\n")] = '\0';
  doi[strcspn(doi, "\r")] = '\0';
  printf("DOI %s removido\n", doi);
  p_no atual = primeiro;
  p_no anterior = NULL;
  int flag2 = 0;
  do {
    if (atual == flag){
      if (anterior!= NULL){
        anterior->prox = atual->prox;
      }
      flag2 =1;
    }
    anterior = atual;
    atual = atual->prox;
  } while(flag2 == 0);

  for ( int numero_autores = 0 ; numero_autores< flag->n_autores;numero_autores++){
    free((flag->autor)[numero_autores]);
  }
  free(flag->autor);
  free(flag->doi);
  if (flag == primeiro){
    primeiro = flag->prox;
  }
  flag->prox = NULL;
  free(flag);

  return primeiro;
}
