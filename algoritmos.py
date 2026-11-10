import unicodedata

from lista import ListaEncadeada
from registro import Registro


def normalizar_texto(texto: str) -> str:
    """Remove acentos e converte o texto para minúsculas.

    Passo a passo:
    1. Aplica a normalização Unicode NFD, que separa cada letra do seu acento.
    2. Descarta os caracteres da categoria "Mn" (marcas combinantes/acentos).
    3. Converte o resultado para minúsculas e o retorna.
    """
    decomposto = unicodedata.normalize("NFD", texto)
    sem_acentos = "".join(
        caractere for caractere in decomposto
        if unicodedata.category(caractere) != "Mn"
    )
    return sem_acentos.lower()


def _buscar_por_atributo(lista: ListaEncadeada, atributo: str, termo: str) -> int:
    """Busca linear por um atributo, imprimindo e retornando o total.

    Passo a passo:
    1. Normaliza o termo de busca (sem acentos e em minúsculas).
    2. Começa no primeiro nó (cabeca).
    3. Enquanto houver nó, normaliza o valor do atributo e verifica se o termo
       está contido nele.
    4. Se estiver, imprime o registro e incrementa o contador.
    5. Avança para o próximo nó.
    6. Retorna o total de registros encontrados.
    """
    termo = normalizar_texto(termo)
    encontrado = 0
    atual = lista.cabeca
    while atual is not None:
        valor = normalizar_texto(getattr(atual.dados, atributo))
        if termo in valor:
            print("-" * 50)
            print(atual.dados)
            encontrado += 1
        atual = atual.proximo
    return encontrado


def buscar_por_titulo(lista: ListaEncadeada, termo: str) -> int:
    """Busca linear por título, ignorando acentos e maiúsculas."""
    return _buscar_por_atributo(lista, "titulo", termo)


def buscar_por_categoria(lista: ListaEncadeada, termo: str) -> int:
    """Busca linear por categoria, ignorando acentos e maiúsculas."""
    return _buscar_por_atributo(lista, "categoria", termo)


def _comparar(criterio: str, reg1: Registro, reg2: Registro) -> bool:
    """Retorna True se reg1 deve vir antes de reg2 no critério."""
    if criterio == "titulo":
        return normalizar_texto(reg1.titulo) < normalizar_texto(reg2.titulo)
    if criterio == "categoria":
        return (normalizar_texto(reg1.categoria)
                < normalizar_texto(reg2.categoria))
    if criterio == "horas":
        return reg1.horas < reg2.horas
    return False


def ordenar_lista(lista: ListaEncadeada, criterio: str) -> None:
    """Ordena a lista encadeada pelo critério (Selection Sort).

    Passo a passo:
    1. Se a lista estiver vazia ou tiver um único nó, não há nada a ordenar.
    2. Para cada nó (início), assume que ele contém o menor registro.
    3. Percorre o restante da lista e compara cada registro com o menor atual.
    4. Se encontrar um registro menor, guarda o nó encontrado.
    5. Ao final do laço interno, troca os dados do nó início com o menor.
    6. Avança para o próximo nó e repete até o fim da lista.

    Troca apenas os dados entre nós, mantendo as referências intactas.
    """
    if lista.cabeca is None or lista.cabeca.proximo is None:
        return

    inicio = lista.cabeca
    while inicio is not None:
        menor = inicio
        atual = inicio.proximo
        while atual is not None:
            if _comparar(criterio, atual.dados, menor.dados):
                menor = atual
            atual = atual.proximo
        if menor is not inicio:                 # troca só os dados
            inicio.dados, menor.dados = menor.dados, inicio.dados
        inicio = inicio.proximo