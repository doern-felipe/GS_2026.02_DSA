# Algoritmos do Colabre: busca linear e Selection Sort

Este documento explica os algoritmos de **busca** e **ordenação** do Colabre
(Citizen Assist AI, recorte de banco de tempo e serviços comunitários). Todos
foram escritos pela equipe e operam sobre a **lista encadeada própria** do
projeto, sem funções prontas de busca ou ordenação.

| Algoritmo | Onde está | Para que serve |
|-----------|-----------|----------------|
| Busca linear por ID | `lista.py` (`buscar_por_id`) | Consultar, atualizar, excluir e impedir ID duplicado |
| Busca linear por título ou categoria | `algoritmos.py` (`_buscar_por_atributo`, `buscar_por_titulo`, `buscar_por_categoria`) | Pesquisar registros por trecho de texto |
| Selection Sort | `algoritmos.py` (`ordenar_lista`, `_comparar`) | Ordenar por título, categoria ou horas |

---

## 1. Busca linear

A busca linear percorre a lista **nó a nó**, a partir da cabeça, até encontrar o
que procura ou chegar ao fim (`proximo` igual a `None`). Em uma lista encadeada
não há índices, então percorrer os nós em sequência é a forma natural de buscar.

### 1.1 Busca por ID (`buscar_por_id`)

1. A variável `atual` começa em `cabeca`.
2. Enquanto `atual` não for `None`:
   - se `atual.dados.id` for igual ao ID procurado, **retorna o registro
     imediatamente**;
   - senão, `atual` avança para `atual.proximo`.
3. Se chegar ao fim sem achar, retorna `None`.

Ela é usada na consulta, na atualização, na exclusão e no cadastro (para recusar
ID duplicado).

### 1.2 Busca por título ou categoria (`_buscar_por_atributo`)

As funções públicas `buscar_por_titulo` e `buscar_por_categoria` chamam
`_buscar_por_atributo(lista, atributo, termo)`, que funciona assim:

1. O termo é **normalizado** por `normalizar_texto`: remove acentos e converte
   para minúsculas. Assim, `"educacao"` encontra `"Educação"`.
2. `atual` começa em `cabeca` e o contador de resultados começa em `0`.
3. Enquanto `atual` não for `None`:
   - normaliza o atributo do registro (título ou categoria);
   - se o termo estiver **contido** no atributo (operador `in`), imprime o
     registro e incrementa o contador;
   - `atual` avança para `atual.proximo`.
4. Retorna o total de registros encontrados.

Diferente da busca por ID, **não para no primeiro resultado**: ela precisa
listar todos os registros que combinam, então sempre percorre a lista inteira.

### 1.3 Exemplo com 4 registros

Lista, buscando o termo `"educacao"` por título:

| Nó | Título | Normalizado | Contém `"educacao"`? |
|----|--------|-------------|----------------------|
| 1 | Educação | `educacao` | Sim, imprime |
| 2 | Informática | `informatica` | Não |
| 3 | Horta | `horta` | Não |
| 4 | Educação Infantil | `educacao infantil` | Sim, imprime |

A função imprime os nós 1 e 4 e retorna `2`.

### 1.4 Consulta sem resultado

- **Busca por título ou categoria:** se nenhum registro combinar, o contador
  fica em `0`, a função retorna `0` e o menu mostra *"Nenhum registro
  encontrado."*.
- **Consulta por ID:** `buscar_por_id` retorna `None` e o menu mostra
  *"Registro não encontrado (ID x)."*.
- **Lista vazia:** o menu avisa que a lista está vazia antes de chamar a busca.

Em nenhum caso o programa gera erro.

### 1.4.1 Por que não usar busca binária

A busca binária depende de acesso direto ao elemento do meio, o que um vetor
oferece em `O(1)`. Na lista encadeada não existe índice: chegar ao meio exige
percorrer os nós, e mesmo no melhor cenário o deslocamento total soma
`n/2 + n/4 + ... = O(n)`. Ou seja, **não há ganho** sobre a busca linear, e o
código ficaria mais complexo. Além disso, a lista não está necessariamente
ordenada. Por isso a busca linear é a escolha adequada.

### 1.5 Complexidade da busca

| Busca | Melhor | Médio | Pior | Explicação |
|-------|--------|-------|------|------------|
| Por ID (`buscar_por_id`) | `O(1)` | `O(n)` | `O(n)` | Para ao achar. Melhor caso: ID na cabeça. Pior: no fim ou inexistente. |
| Por título/categoria (`_buscar_por_atributo`) | `O(n)` | `O(n)` | `O(n)` | Lista todos os resultados, então percorre sempre a lista inteira. |

O custo de `normalizar_texto` em cada nó depende do tamanho do texto, que é
limitado pelos tamanhos máximos dos campos do registro, portanto é constante.

---

## 2. Selection Sort

A ordenação é feita por **Selection Sort** em `ordenar_lista(lista, criterio)`,
com `criterio` igual a `"titulo"`, `"categoria"` ou `"horas"`. A comparação é
feita por `_comparar(criterio, reg1, reg2)`, que retorna `True` se `reg1` deve
vir antes de `reg2`. Para textos, a comparação usa o texto **normalizado**, de
modo que acentos e maiúsculas não atrapalhem a ordem alfabética.

### 2.1 Como funciona

1. Se a lista estiver vazia ou tiver um único nó, não há nada a fazer.
2. A variável `inicio` percorre cada nó da lista.
3. Para cada `inicio`, assume-se que ele contém o **menor** registro (`menor`).
4. A variável `atual` percorre os nós seguintes. Sempre que `_comparar`
   indicar que o registro de `atual` vem antes do de `menor`, `menor` passa a
   ser `atual`.
5. Ao fim do laço interno, se `menor` não for `inicio`, os **dados** dos dois
   nós são trocados (`inicio.dados, menor.dados = menor.dados, inicio.dados`).
6. `inicio` avança para o próximo nó e o processo se repete até o fim.

A lista é ordenada **no lugar**: depois da ordenação, a própria lista fica na
nova ordem. A troca mexe só nos dados dos nós, então as referências `proximo`
nunca mudam e a estrutura da lista não corre risco de quebrar.

### 2.2 Exemplo passo a passo (4 registros)

Ordenando por `horas` crescente. Estado inicial:

```
30 → 10 → 20 → 5
```

**Passo 1:** `inicio` é o nó `30`. Percorre `10`, `20`, `5`; o menor é `5`.
Troca os dados de `30` e `5`:

```
5 → 10 → 20 → 30
```

**Passo 2:** `inicio` é o nó `10`. Percorre `20`, `30`; o menor é o próprio
`10`. Nenhuma troca.

**Passo 3:** `inicio` é o nó `20`. Percorre `30`; o menor é o próprio `20`.
Nenhuma troca.

**Passo 4:** `inicio` é o último nó. Não há nós depois dele; fim.

Resultado final:

```
5 → 10 → 20 → 30
```

Foram feitas `3 + 2 + 1 = 6` comparações, que é `n(n-1)/2` para `n = 4`, e
uma única troca.

### 2.3 Por que essa escolha

- É **simples** de implementar e de explicar em uma lista encadeada.
- Troca apenas os **dados** dos nós, então **não altera as referências**
  `proximo` e não corre o risco de perder nós.
- Faz poucas trocas (no máximo `n - 1`), apesar de muitas comparações.

### 2.4 Complexidade

| Caso | Tempo | Explicação |
|------|-------|------------|
| Melhor | `O(n²)` | Mesmo com a lista já ordenada, o laço interno percorre todos os nós restantes. |
| Médio | `O(n²)` | Sempre `n(n-1)/2` comparações. |
| Pior | `O(n²)` | Lista invertida: mesmo número de comparações. |
| Espaço | `O(1)` | Usa apenas referências auxiliares (`inicio`, `menor`, `atual`). |

O número de comparações não depende da ordem inicial dos dados. Já o número de
trocas é no máximo `n - 1`.

### 2.5 Por que não é estável

Um algoritmo é **estável** quando preserva a ordem relativa de elementos
iguais. O Selection Sort **não é estável**, porque a troca de dados pode fazer
um elemento passar por cima de outro igual.

Exemplo com `2a` e `2b` iguais (`2a` vem antes de `2b`) e um `1`:

```
2a → 2b → 1
```

- Passo 1: o menor é `1`. Troca `2a` com `1`:

```
1 → 2b → 2a
```

- Passos seguintes: não há mais trocas.

A ordem relativa de `2a` e `2b` foi **invertida**. Para o Colabre isso é
aceitável: registros com o mesmo valor no critério (por exemplo, a mesma
quantidade de horas) podem aparecer em qualquer ordem entre si.

---

## 3. Auditoria: nada de funções prontas

Nenhum arquivo do projeto usa ordenação ou busca prontas:

- `sorted()`: não é usado.
- `list.sort()` (`.sort()`): não é usado.
- `heapq` e `bisect`: não são importados.
- `min()` e `max()`: não são usados para ordenar.

A única ordenação é o **Selection Sort** escrito à mão em `ordenar_lista`, e as
buscas são laços `while` que percorrem os nós.

**Comparação de texto** (`algoritmos.py`):

- `normalizar_texto` remove acentos e converte para minúsculas antes de
  comparar.
- `_buscar_por_atributo` usa `in` apenas para verificar se o termo está contido
  no texto de um campo (a busca em si é o laço sobre os nós).
- `_comparar` usa o operador `<` sobre textos normalizados para definir a ordem
  no Selection Sort.

**Uso de `dict`:** limitado a dois pontos em `menu.py`, e nenhum guarda
registros:

- `analise`: conta a quantidade de registros por categoria durante a análise.
- `ordenar_e_exibir`: traduz a opção do menu no critério de ordenação.

Os registros ficam **exclusivamente** na `ListaEncadeada`; nenhum é guardado em
`list`, `dict`, `set` ou estrutura similar.