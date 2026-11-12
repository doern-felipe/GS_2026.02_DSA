"""Demonstração do Colabre: mostra os nós da lista encadeada funcionando.

Executar:  python demo.py      (Enter avança cada etapa)
"""

from algoritmos import buscar_por_titulo, ordenar_lista
from lista import ListaEncadeada
from menu import analise
from registro import Registro


def pausa(texto: str) -> None:
    """Espera o Enter para avançar (facilita a gravação)."""
    try:
        input(f"\n[Enter] {texto} ")
    except EOFError:
        pass


def endereco(no) -> str:
    """Endereço curto do nó (últimos dígitos), para mostrar as referências."""
    return "None" if no is None else "@" + hex(id(no))[-5:]


def mostrar_nos(lista: ListaEncadeada, titulo: str) -> None:
    """Percorre a lista e mostra cada nó, o registro dentro dele e o próximo."""
    print(f"\n=== {titulo} (tamanho = {lista.tamanho}) ===")
    print(f"cabeca -> {endereco(lista.cabeca)}")
    atual = lista.cabeca
    while atual is not None:
        dados = atual.dados
        print(f"  {endereco(atual)} | registro {dados.id} | "
              f"{dados.titulo[:22]:<22} | {dados.horas}h | "
              f"proximo -> {endereco(atual.proximo)}")
        atual = atual.proximo


def novo(id: int, titulo: str, categoria: str, horas: int) -> Registro:
    """Cria um registro de demonstração."""
    return Registro(id, titulo, "Oferta", categoria, "Descrição",
                    "Requisitos", "Local", horas, "Responsável")


def main() -> None:
    lista = ListaEncadeada()
    mostrar_nos(lista, "1. Lista nova, vazia")
    pausa("inserir 5 registros no fim")

    for registro in (novo(1, "Aula de inglês", "Educação", 3),
                     novo(2, "Conserto de torneira", "Manutenção", 1),
                     novo(3, "Horta comunitária", "Horta", 4),
                     novo(4, "Reforço de matemática", "Educação", 5),
                     novo(5, "Oficina de culinária", "Culinária", 2)):
        lista.inserir_fim(registro)
    mostrar_nos(lista, "2. Depois de inserir 5 registros")
    pausa("buscar")

    print("\n=== 3. Busca linear ===")
    print("Título 'INGLES' (sem acento e em maiúsculas):")
    print(f"-> {buscar_por_titulo(lista, 'INGLES')} resultado(s)")
    print("\nTítulo 'xyz':")
    print(f"-> {buscar_por_titulo(lista, 'xyz')} resultado(s) (sem resultado)")
    pausa("ordenar por horas")

    mostrar_nos(lista, "4. Antes de ordenar")
    ordenar_lista(lista, "horas")
    mostrar_nos(lista, "4. Depois de ordenar por horas (Selection Sort)")
    print("\nRepare: os endereços e as ligações são os mesmos; "
          "só os dados trocaram de nó.")
    pausa("remover cabeça, meio, fim e um ID inexistente")

    for id, onde in ((2, "cabeça"), (1, "meio"), (4, "fim"), (99, "inexistente")):
        print(f"\nremover_por_id({id}) [{onde}] -> {lista.remover_por_id(id)}")
        mostrar_nos(lista, f"5. Depois de remover_por_id({id})")
    pausa("indicadores")

    analise(lista)
    pausa("limpar a lista")

    lista.limpar()
    mostrar_nos(lista, "6. Depois de limpar()")


if __name__ == "__main__":
    main()
