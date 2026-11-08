#ifndef REGISTRO_H
#define REGISTRO_H

typedef struct {
    int id;                     // identificador único
    char titulo[100];           // titulo + \0
    char tipo[10];              // oferta, pedido ou projeto + \0
    char categoria[50];         // ex.: educacao, informatica + \0
    char descricao[200];        // descricao + \0
    char requisitos[150];       // pre-requisitos + \0
    char local[100];            // local + \0
    int horas;                  // horas de ajuda (creditos)
    char responsavel[60];       // responsavel + \0
} Registro;

#endif