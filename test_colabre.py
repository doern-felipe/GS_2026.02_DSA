"""Testes do Colabre: casos normais, inexistentes, inválidos e lista vazia.

Só biblioteca padrão. Executar na pasta do projeto:  python -m unittest -v
"""

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import menu
from algoritmos import buscar_por_categoria, buscar_por_titulo, ordenar_lista
from lista import ListaEncadeada
from registro import Registro


def reg(id, titulo="T", categoria="Educação", horas=1):
    """Cria um Registro de teste."""
    return Registro(id, titulo, "Oferta", categoria, "Desc", "Req", "Local",
                    horas, "Resp")


def lista_com(*registros):
    """Cria uma lista e insere os registros, na ordem."""
    lista = ListaEncadeada()
    for registro in registros:
        lista.inserir_fim(registro)
    return lista


def campo(lista, nome):
    """Valores de um campo, na ordem da lista (percorre os nós)."""
    valores, atual = [], lista.cabeca
    while atual is not None:
        valores.append(getattr(atual.dados, nome))
        atual = atual.proximo
    return valores


def rodar(funcao, *args, entradas=None, **kwargs):
    """Roda a função com input simulado; retorna (resultado, saída)."""
    saida = io.StringIO()
    simulado = entradas or AssertionError("não deveria pedir entrada")
    with redirect_stdout(saida), patch("builtins.input", side_effect=simulado):
        resultado = funcao(*args, **kwargs)
    return resultado, saida.getvalue()


class TestLista(unittest.TestCase):
    def test_inserir_mantem_ordem_e_tamanho(self):
        """Inserir 1, 2, 3 -> lista 1,2,3 e tamanho 3."""
        lista = lista_com(reg(1), reg(2), reg(3))
        self.assertEqual(campo(lista, "id"), [1, 2, 3])
        self.assertEqual(lista.tamanho, 3)

    def test_remover_cabeca_meio_e_fim(self):
        """Remover 1 (cabeça), 2 (meio) ou 3 (fim) de [1,2,3] -> True e a
        lista fica sem esse ID, com tamanho 2."""
        for id in (1, 2, 3):
            with self.subTest(id=id):
                lista = lista_com(reg(1), reg(2), reg(3))
                self.assertTrue(lista.remover_por_id(id))
                esperado = [i for i in (1, 2, 3) if i != id]
                self.assertEqual(campo(lista, "id"), esperado)
                self.assertEqual(lista.tamanho, 2)

    def test_remover_id_inexistente(self):
        """Remover 99 de [1,2] -> False e lista intacta."""
        lista = lista_com(reg(1), reg(2))
        self.assertFalse(lista.remover_por_id(99))
        self.assertEqual(campo(lista, "id"), [1, 2])

    def test_remover_em_lista_vazia(self):
        """Remover 1 de lista vazia -> False, sem erro."""
        lista = ListaEncadeada()
        self.assertFalse(lista.remover_por_id(1))
        self.assertEqual(lista.tamanho, 0)


class TestBuscaOrdenacao(unittest.TestCase):
    def setUp(self):
        self.lista = lista_com(reg(1, "Aula de inglês", "Educação", 2),
                               reg(2, "Conserto de torneira", "Manutenção", 1),
                               reg(3, "Horta comunitária", "Horta", 4))

    def test_buscar_por_id(self):
        """ID 3 -> 'Horta comunitária'; ID 99 -> None."""
        self.assertEqual(self.lista.buscar_por_id(3).titulo,
                         "Horta comunitária")
        self.assertIsNone(self.lista.buscar_por_id(99))

    def test_busca_por_titulo_ignora_acento_e_maiuscula(self):
        """Título 'INGLES' -> 1 resultado ('Aula de inglês')."""
        total, saida = rodar(buscar_por_titulo, self.lista, "INGLES")
        self.assertEqual(total, 1)
        self.assertIn("Aula de inglês", saida)

    def test_busca_sem_resultado(self):
        """Categoria 'culinaria' -> 0 resultados e nenhuma saída."""
        total, saida = rodar(buscar_por_categoria, self.lista, "culinaria")
        self.assertEqual((total, saida), (0, ""))

    def test_ordenar_por_horas(self):
        """Horas 2,1,4 ordenadas -> 1,2,4."""
        ordenar_lista(self.lista, "horas")
        self.assertEqual(campo(self.lista, "horas"), [1, 2, 4])

    def test_ordenar_por_titulo_ignora_acentos(self):
        """Zebra, Água, banana -> Água, banana, Zebra, sem perder nós."""
        lista = lista_com(reg(1, "Zebra"), reg(2, "Água"), reg(3, "banana"))
        ordenar_lista(lista, "titulo")
        self.assertEqual(campo(lista, "titulo"), ["Água", "banana", "Zebra"])
        self.assertEqual(len(campo(lista, "id")), lista.tamanho)

    def test_ordenar_lista_vazia_e_com_um_registro(self):
        """Ordenar lista vazia e com 1 registro -> sem erro, nada muda."""
        vazia = ListaEncadeada()
        ordenar_lista(vazia, "horas")
        self.assertIsNone(vazia.cabeca)
        um = lista_com(reg(1))
        ordenar_lista(um, "horas")
        self.assertEqual(campo(um, "id"), [1])


class TestEntradas(unittest.TestCase):
    def test_opcao_de_menu_invalida(self):
        """'abc', '', '9', '-1' e depois '3' -> 4 avisos e retorna 3."""
        opcao, saida = rodar(menu.ler_opcao_menu,
                             entradas=["abc", "", "9", "-1", "3"])
        self.assertEqual(opcao, 3)
        self.assertEqual(saida.count("Opção inválida"), 4)

    def test_id_com_texto_e_negativo(self):
        """ID 'abc', '-5' e depois '7' -> rejeita os dois e retorna 7."""
        id, saida = rodar(menu.ler_id, ListaEncadeada(),
                          entradas=["abc", "-5", "7"])
        self.assertEqual(id, 7)
        self.assertIn("Entrada inválida", saida)
        self.assertIn("no mínimo 0", saida)

    def test_id_duplicado(self):
        """ID 1 já existe: '1' e depois '2' -> 'já é usado' e retorna 2."""
        id, saida = rodar(menu.ler_id, lista_com(reg(1)), entradas=["1", "2"])
        self.assertEqual(id, 2)
        self.assertIn("já é usado", saida)

    def test_campo_vazio_e_texto_acima_do_limite(self):
        """'', 'abcdefg' (limite 5) e 'ok' -> rejeita os dois, retorna 'ok'."""
        texto, saida = rodar(menu.ler_texto, "Título", max_len=5,
                             entradas=["", "abcdefg", "ok"])
        self.assertEqual(texto, "ok")
        self.assertIn("não pode ficar vazio", saida)
        self.assertIn("no máximo 5", saida)

    def test_horas_zero_negativa_e_texto(self):
        """Horas '0', '-3', 'abc' e '4' -> 2 avisos 'no mínimo 1', retorna 4."""
        horas, saida = rodar(menu.ler_inteiro, "Horas", minimo=1,
                             entradas=["0", "-3", "abc", "4"])
        self.assertEqual(horas, 4)
        self.assertEqual(saida.count("no mínimo 1"), 2)
        self.assertIn("Entrada inválida", saida)

    def test_tipo_invalido_e_qualquer_caixa(self):
        """'Doação' -> inválido; 'PEDIDO' -> 'Pedido'; ao atualizar, 'oferta'
        -> 'Oferta'."""
        tipo, saida = rodar(menu.ler_tipo, entradas=["Doação", "PEDIDO"])
        self.assertEqual(tipo, "Pedido")
        self.assertIn("Tipo inválido", saida)
        novo, _ = rodar(menu.ler_tipo_opcional, "Pedido", entradas=["oferta"])
        self.assertEqual(novo, "Oferta")

    def test_cadastro_completo(self):
        """Cadastro válido com tipo 'oferta' -> 1 registro com tipo 'Oferta'."""
        lista = ListaEncadeada()
        entradas = ["1", "Aula de inglês", "oferta", "Educação", "Conversação",
                    "Nenhum", "Online", "2", "Ana", "n"]
        rodar(menu.cadastrar_registro, lista, entradas=entradas)
        self.assertEqual(len(lista), 1)
        self.assertEqual(lista.buscar_por_id(1).tipo, "Oferta")


class TestListaVazia(unittest.TestCase):
    def test_opcoes_2_a_7_avisam_sem_pedir_dados(self):
        """Opções 2 a 7 com lista vazia -> 'A lista está vazia', sem input."""
        for opcao in range(2, 8):
            with self.subTest(opcao=opcao):
                _, saida = rodar(menu.executar_opcao, ListaEncadeada(), opcao)
                self.assertIn("A lista está vazia", saida)

    def test_main_encerra_com_zero_e_com_ctrl_d(self):
        """main() com '0' e com Ctrl+D -> encerra com mensagem, sem erro."""
        for entradas in (["0"], EOFError()):
            with self.subTest(entradas=entradas):
                _, saida = rodar(menu.main, entradas=entradas)
                self.assertIn("Encerrando o programa.", saida)


if __name__ == "__main__":
    unittest.main(verbosity=2)