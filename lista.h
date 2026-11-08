#ifndef LISTA_H
#define LISTA_H
#include "registro.h"

typedef struct No {
    Registro dados;         // registro guardado neste no
    struct No *proximo;     // endereço do proximo no (NULL no fim)
} No;

typedef struct {
    No *cabeca;     // primeiro no
    int tamanho;    // quantidade de nos
} Lista;

Lista criar_lista(void);
No *criar_no(Registro dados);

#endif