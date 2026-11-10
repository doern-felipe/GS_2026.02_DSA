from registro import Registro
from lista import ListaEncadeada
from algoritmos import buscar_por_categoria, buscar_por_titulo


TIPOS_VALIDOS = ("Oferta", "Pedido", "Projeto")


def ler_texto(campo: str) -> str:
    """Lê um texto não vazio do terminal."""
    while True:
        try:
            valor = input(f"{campo}: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEntrada interrompida. Tente novamente.")
            continue
        if valor == "":
            print(f"O campo '{campo}' não pode ficar vazio.")
            continue
        return valor


def ler_inteiro_positivo(campo: str) -> int:
    """Lê um número inteiro maior que zero."""
    while True:
        try:
            valor = int(input(f"{campo}: ").strip())
        except ValueError:
            print(f"O campo '{campo}' deve ser um número inteiro.")
            continue
        except (EOFError, KeyboardInterrupt):
            print("\nEntrada interrompida. Tente novamente.")
            continue
        if valor <= 0:
            print(f"O campo '{campo}' deve ser maior que zero.")
            continue
        return valor


def ler_tipo() -> str:
    """Lê o tipo, aceitando apenas Oferta, Pedido ou Projeto."""
    while True:
        valor = ler_texto("Tipo (Oferta/Pedido/Projeto)")
        if valor in TIPOS_VALIDOS:
            return valor
        print("Tipo inválido. Digite Oferta, Pedido ou Projeto.")


def ler_id(lista: ListaEncadeada) -> int:
    """Lê um ID inteiro que ainda não exista na lista."""
    while True:
        try:
            id = int(input("ID: ").strip())
        except ValueError:
            print("O ID deve ser um número inteiro.")
            continue
        except (EOFError, KeyboardInterrupt):
            print("\nEntrada interrompida. Tente novamente.")
            continue
        if lista.buscar_por_id(id) is not None:
            print(f"O ID {id} já existe. Escolha outro.")
            continue
        return id


def cadastrar_registro(lista: ListaEncadeada) -> None:
    """Lê os campos, valida e insere; permite cadastrar vários em sequência."""
    while True:
        print("\n--- Cadastro de Registro ---")
        id = ler_id(lista)
        titulo = ler_texto("Título")
        tipo = ler_tipo()
        categoria = ler_texto("Categoria")
        descricao = ler_texto("Descrição")
        requisitos = ler_texto("Requisitos")
        local = ler_texto("Local")
        horas = ler_inteiro_positivo("Horas")
        responsavel = ler_texto("Responsável")

        registro = Registro(id, titulo, tipo, categoria, descricao,
                            requisitos, local, horas, responsavel)
        lista.inserir_fim(registro)
        print(f"Registro '{titulo}' cadastrado com sucesso!")

        try:
            resposta = input("Cadastrar outro? (s/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nEntrada interrompida. Encerrando cadastro.")
            break
        if resposta != "s":
            break

def ler_inteiro(campo: str) -> int:
    """Lê um número inteiro do terminal."""
    while True:
        try:
            return int(input(f"{campo}: ").strip())
        except ValueError:
            print(f"O campo '{campo}' deve ser um número inteiro.")
        except (EOFError, KeyboardInterrupt):
            print("\nEntrada interrompida. Tente novamente.")


def consultar_por_id(lista: ListaEncadeada) -> None:
    """Consulta um registro pelo ID e exibe todos os campos."""
    if len(lista) == 0:                     # lista vazia: avisa antes de pedir
        print("A lista está vazia. Nenhum registro para consultar.")
        return

    id = ler_inteiro("ID para consulta")
    registro = lista.buscar_por_id(id)
    print()
    if registro is None:
        print(f"Registro não encontrado (ID {id}).")
    else:
        print("--- Registro encontrado ---")
        print(registro)                     # usa o __str__ de Registro


def pesquisar(lista: ListaEncadeada) -> None:
    """Submenu de pesquisa por título ou categoria."""
    if len(lista) == 0:                     # lista vazia
        print("A lista está vazia. Nenhum registro para pesquisar.")
        return

    print("\n--- Pesquisar ---")
    print("1 - Por título")
    print("2 - Por categoria")
    print("0 - Voltar")
    opcao = ler_inteiro("Opção")

    if opcao == 0:
        return
    if opcao == 1:
        termo = ler_texto("Título (termo de busca)")
        print("\n--- Resultado da pesquisa por título ---")
        total = buscar_por_titulo(lista, termo)
    elif opcao == 2:
        termo = ler_texto("Categoria (termo de busca)")
        print("\n--- Resultado da pesquisa por categoria ---")
        total = buscar_por_categoria(lista, termo)
    else:
        print("Opção inválida.")
        return

    if total == 0:
        print("Nenhum registro encontrado.")
    else:
        print("-" * 50)
        print(f"Total de registros encontrados: {total}")