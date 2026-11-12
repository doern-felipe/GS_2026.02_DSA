# Análise Big-O e contexto CitizenTech

Este documento analisa a complexidade das operações do Colabre **de acordo com
a implementação real** (`lista.py`, `algoritmos.py` e `menu.py`) e relaciona o
projeto ao contexto CitizenTech e aos ODS.

---

## 1. Análise Big-O

### 1.1 Convenções

- **n**: quantidade de registros (nós) na lista, guardada em `tamanho`.
- **c**: quantidade de categorias distintas (`c ≤ n`).
- Os campos de texto têm tamanho máximo (título 100, categoria 50 etc.), então
  cada chamada de `normalizar_texto`, cada comparação de texto e cada `in`
  entre campos custa tempo **constante**, `O(1)`.
- O termo digitado na pesquisa não tem limite de tamanho no código; assume-se
  que é curto e, portanto, tratado como constante.
- Contam-se operações sobre os nós. O tempo de digitação do usuário não entra.
- **Caso médio** de busca bem-sucedida: o registro está, em média, no meio da
  lista (cerca de `n/2` nós visitados), o que continua sendo `O(n)`.

### 1.2 Tabela

| Operação | Onde | Melhor | Médio | Pior | Espaço |
|----------|------|--------|-------|------|--------|
| Inserção no fim (`inserir_fim`) | `lista.py` | `O(1)` | `O(n)` | `O(n)` | `O(1)` |
| Percurso (`imprimir_lista`) | `lista.py` | `O(n)` | `O(n)` | `O(n)` | `O(1)` |
| Busca por ID (`buscar_por_id`) | `lista.py` | `O(1)` | `O(n)` | `O(n)` | `O(1)` |
| Busca por título/categoria (`_buscar_por_atributo`) | `algoritmos.py` | `O(n)` | `O(n)` | `O(n)` | `O(1)` |
| Remoção (`remover_por_id`) | `lista.py` | `O(1)` | `O(n)` | `O(n)` | `O(1)` |
| Ordenação (Selection Sort, `ordenar_lista`) | `algoritmos.py` | `O(n²)` | `O(n²)` | `O(n²)` | `O(1)` |
| Atualização (`atualizar_registro`) | `menu.py` | `O(1)` | `O(n)` | `O(n)` | `O(1)` |
| Análise (`analise`) | `menu.py` | `O(n)` | `O(n)` | `O(n)` | `O(c)`, até `O(n)` |
| Limpeza (`limpar`) | `lista.py` | `O(n)` | `O(n)` | `O(n)` | `O(1)` |
| Tamanho (`__len__`) | `lista.py` | `O(1)` | `O(1)` | `O(1)` | `O(1)` |

### 1.3 Justificativas

**Inserção no fim (`inserir_fim`).** Como a lista **não tem referência para a
cauda**, é preciso chegar ao último nó. O laço
`while atual.proximo is not None` executa `n - 1` vezes quando a lista já tem
`n` nós, o que dá `O(n)` no caso médio e no pior. O melhor caso é a lista
vazia: só atribui `cabeca = novo_no`, sem laço, em `O(1)`. O espaço é `O(1)`:
um nó novo e uma referência auxiliar (`atual`).

**Percurso (`imprimir_lista`).** O laço `while atual is not None` visita cada
nó uma vez, com impressão de tamanho fixo por nó. É `O(n)` em todos os casos e
`O(1)` de espaço. Com a lista vazia, mostra a mensagem e retorna (`O(1)`).

**Busca por ID (`buscar_por_id`).** O laço `while atual is not None` retorna
assim que encontra o ID. No melhor caso, o ID está na cabeça (`O(1)`). No caso
médio visita cerca de `n/2` nós, e no pior caso (ID no último nó ou
inexistente) visita os `n` nós, ambos `O(n)`. Espaço `O(1)`: só a variável
`atual`.

**Busca por título/categoria (`_buscar_por_atributo`).** O laço
`while atual is not None` **não para no primeiro resultado**, porque precisa
listar todos os que combinam. Por isso executa `n` iterações em qualquer
situação: `O(n)` no melhor, no médio e no pior caso. Em cada iteração há uma
chamada de `normalizar_texto` e um `in` (constantes, ver 1.1) e, se houver
correspondência, uma impressão. O espaço é `O(1)`: o contador, a referência
`atual` e as cópias normalizadas dos textos, de tamanho limitado.

**Remoção (`remover_por_id`).** Na lista vazia ou com o ID na cabeça, não há
laço (`O(1)`). Nos demais casos, o laço `while atual is not None` avança com as
referências `anterior` e `atual`: visita cerca de `n/2` nós no caso médio e até
`n - 1` nós no pior (último nó ou ID inexistente), ou seja, `O(n)`. A ligação
`anterior.proximo = atual.proximo` e o desligamento do nó removido são `O(1)`.
Espaço `O(1)`: `removido`, `anterior` e `atual`.

**Ordenação (Selection Sort, `ordenar_lista`).** Com `n ≥ 2`, o laço externo
`while inicio is not None` percorre os `n` nós e, para cada um, o laço interno
`while atual is not None` percorre os nós seguintes. O total é
`(n-1) + (n-2) + ... + 1 = n(n-1)/2` comparações, **independentemente da
ordem inicial**, então `O(n²)` no melhor, médio e pior caso. Cada comparação
(`_comparar`) é `O(1)` pelos limites dos campos. As trocas são no máximo
`n - 1`, e cada uma só troca duas referências para `Registro`
(`inicio.dados, menor.dados = menor.dados, inicio.dados`), em `O(1)`. Com
`n ≤ 1`, a função retorna logo no início (`O(1)`). Espaço `O(1)`: `inicio`,
`menor` e `atual`, sem lista auxiliar.

**Atualização (`atualizar_registro`).** O custo vem de `buscar_por_id`:
`O(1)` com o ID na cabeça e `O(n)` no caso médio e no pior. Depois disso, a
função só lê e altera um número fixo de campos do próprio registro, em `O(1)`,
e **não mexe nas referências** da lista. Espaço `O(1)`.

**Análise (`analise`).** O laço `while atual is not None` percorre os `n` nós
uma vez, e em cada um faz `normalizar_texto` (`O(1)`) e uma consulta/inserção
no `dict` `categorias`, de tempo médio constante. Depois, um laço sobre
`categorias.values()` imprime as `c` categorias. O total é `O(n + c) = O(n)`
em todos os casos. É a única operação com espaço que depende da entrada: o
`dict` guarda uma entrada por categoria distinta, `O(c)`, chegando a `O(n)` se
todas as categorias forem diferentes. Ele guarda só nomes de categorias e
contagens; os registros continuam apenas na lista encadeada.

**Limpeza (`limpar`).** O laço `while atual is not None` desliga cada nó
(`atual.proximo = None`) e avança, visitando os `n` nós: `O(n)` em todos os
casos, com espaço `O(1)` (`atual` e `proximo`). O menu não chama `limpar`; o
método fica disponível para testes e demonstração.

**Tamanho (`__len__`).** Retorna o contador `tamanho`, mantido a cada inserção
e remoção, em `O(1)`. É por isso que o menu verifica "lista vazia" sem percorrer
a lista.

### 1.4 Custo das opções do menu

| Opção do menu | Chamadas principais | Custo |
|---------------|---------------------|-------|
| 1 Cadastrar | `buscar_por_id` (em `ler_id`) + `inserir_fim` | `O(n)` por tentativa de ID |
| 2 Consultar por ID | `buscar_por_id` | `O(1)` no melhor caso; `O(n)` no médio e no pior |
| 3 Pesquisar | `_buscar_por_atributo` | `O(n)` |
| 4 Atualizar | `buscar_por_id` | `O(1)` no melhor caso; `O(n)` no médio e no pior |
| 5 Excluir | `buscar_por_id` + `remover_por_id` | `O(1)` no melhor caso; `O(n)` no médio e no pior (duas passagens, `2n` continua `O(n)`) |
| 6 Ordenar e exibir | `ordenar_lista` + `imprimir_lista` | `O(n²)` |
| 7 Análise | `analise` | `O(n)` |

### 1.5 Observações

- A inserção é `O(n)` porque a lista **não guarda referência para a cauda**,
  por simplicidade. Com uma referência para o último nó, passaria a `O(1)`.
- O Selection Sort faz `O(n²)` comparações mesmo com a lista já ordenada, mas
  só no máximo `n - 1` trocas. Um Merge Sort traria `O(n log n)`, ao custo de
  um código mais complexo.
- A busca é linear porque a lista encadeada não tem acesso por índice; a busca
  binária não traria ganho (ver `docs/algoritmos.md`).

---

## 2. Colabre e o contexto CitizenTech

Muita gente tem tempo e conhecimento para oferecer, mas não encontra quem
precise, enquanto outras pessoas não conseguem pagar por aulas, reparos ou
orientação. O Colabre atende moradores de comunidades e condomínios, sobretudo
quem tem pouca renda, com a regra de que 1 hora de ajuda equivale a 1 crédito.
No **ODS 4** (educação de qualidade), amplia o acesso ao aprendizado: cada
oferta de reforço escolar ou de idiomas vira um registro pesquisável. No
**ODS 10** (redução das desigualdades), permite trocas sem dinheiro, em que uma
hora de inglês vale uma hora de conserto. No **ODS 11** (cidades e comunidades
sustentáveis), os registros do tipo Projeto reúnem vizinhos para revitalizar
praças e montar hortas.