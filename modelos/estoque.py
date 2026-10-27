"""
Regra de negocio: Controle de Estoque de Pecas.

Combinacao de estruturas (documentar no README):
    Lista (produtos) + Fila (lotes de cada produto)
    -> cada Produto guarda uma Fila propria de Lote.
       A baixa de estoque percorre a Lista ate achar o produto e
       consome a Fila do lote mais antigo (FIFO), conforme pedido no
       enunciado ("a saida deve sempre consumir primeiro o lote mais
       antigo").
"""

from estruturas.lista import Lista
from estruturas.fila import Fila


class Lote:
    """Um lote de compra de um produto, com data, preco e quantidade."""

    def __init__(self, data_compra, preco_compra, quantidade, data_validade=None):
        self.data_compra = data_compra
        self.preco_compra = preco_compra
        self.quantidade = quantidade
        self.data_validade = data_validade

    def __repr__(self):
        validade = f", val {self.data_validade}" if self.data_validade else ""
        return f"Lote(qtd={self.quantidade}, compra={self.data_compra}{validade})"


class Produto:
    """
    Representa um produto (peca ou fluido) do estoque.

    Cada produto mantem sua propria Fila de lotes. A fila garante que
    o lote inserido primeiro (mais antigo) seja sempre o primeiro a
    ser consumido (FIFO), sem precisar ordenar nada na hora da baixa.
    """

    def __init__(self, nome, codigo, fornecedor, preco_venda, estoque_minimo=0):
        self.nome = nome
        self.codigo = codigo
        self.fornecedor = fornecedor
        self.preco_venda = preco_venda
        self.estoque_minimo = estoque_minimo
        self.lotes = Fila()
        self.perdas = Lista()  # lotes vencidos, descartados e registrados como perda

    def adicionar_lote(self, lote: Lote):
        self.lotes.enfileirar(lote)

    def quantidade_total(self):
        """Soma a quantidade de todos os lotes ainda em estoque (sem remover)."""
        total = 0
        for lote in self.lotes.percorrer():
            total += lote.quantidade
        return total

    def descartar_vencidos(self, data_atual):
        """
        Remove da frente da fila os lotes cuja data de validade ja
        passou, registrando-os como perda. Lotes sem validade (pecas
        que nao vencem) nunca sao descartados por esta rotina.
        Assume que data_atual e as datas de validade sao comparaveis
        (strings no formato AAAA-MM-DD ou objetos date).
        """
        while not self.lotes.esta_vazia():
            frente = self.lotes.espiar()
            if frente.data_validade is not None and frente.data_validade < data_atual:
                vencido = self.lotes.desenfileirar()
                self.perdas.inserir(vencido)
            else:
                break

    def baixar_estoque(self, quantidade_necessaria):
        """
        Consome a quantidade pedida, sempre do lote mais antigo primeiro
        (frente da fila). Se um lote nao for suficiente, passa para o
        proximo. Levanta erro se o total em estoque for insuficiente.
        Retorna a Lista dos lotes (ou fracoes de lote) efetivamente
        consumidos, para fins de rastreabilidade/custo.
        """
        if quantidade_necessaria > self.quantidade_total():
            raise ValueError(
                f"Estoque insuficiente de {self.nome}: "
                f"disponivel {self.quantidade_total()}, solicitado {quantidade_necessaria}"
            )

        consumidos = Lista()
        restante = quantidade_necessaria

        while restante > 0:
            lote = self.lotes.espiar()
            if lote.quantidade <= restante:
                # consome o lote inteiro
                restante -= lote.quantidade
                consumidos.inserir(Lote(lote.data_compra, lote.preco_compra, lote.quantidade, lote.data_validade))
                self.lotes.desenfileirar()
            else:
                # consome parte do lote mais antigo
                lote.quantidade -= restante
                consumidos.inserir(Lote(lote.data_compra, lote.preco_compra, restante, lote.data_validade))
                restante = 0

        return consumidos

    def ajustar_quantidade(self, codigo_lote_data_compra, nova_quantidade):
        """
        Ajuste de inventario: altera a quantidade de um lote especifico,
        identificado pela data de compra (simplificacao razoavel, ja
        que nao ha um id de lote no enunciado).
        """
        for lote in self.lotes.percorrer():
            if lote.data_compra == codigo_lote_data_compra:
                lote.quantidade = nova_quantidade
                return True
        return False

    def abaixo_do_minimo(self):
        return self.quantidade_total() < self.estoque_minimo

    def __repr__(self):
        return f"{self.nome} ({self.codigo}) - {self.quantidade_total()} em estoque"


class ControleEstoque:
    """
    Gerencia a Lista de produtos da oficina.

    Metodos:
        cadastrar_produto(produto)
        buscar_produto(codigo)
        adicionar_lote(codigo, lote)
        baixar_estoque(codigo, quantidade)
        produtos_abaixo_do_minimo()
    """

    def __init__(self):
        self.produtos = Lista()

    def cadastrar_produto(self, produto: Produto):
        if self.buscar_produto(produto.codigo) is not None:
            raise ValueError(f"Ja existe produto cadastrado com codigo {produto.codigo}")
        self.produtos.inserir(produto)

    def buscar_produto(self, codigo):
        return self.produtos.buscar(lambda p: p.codigo == codigo)

    def adicionar_lote(self, codigo, lote: Lote):
        """Percorre a Lista ate achar o produto e enfileira o novo lote."""
        produto = self.buscar_produto(codigo)
        if produto is None:
            raise ValueError(f"Produto com codigo {codigo} nao encontrado")
        produto.adicionar_lote(lote)

    def baixar_estoque(self, codigo, quantidade):
        """Percorre a Lista ate o produto e consome a Fila do lote mais antigo."""
        produto = self.buscar_produto(codigo)
        if produto is None:
            raise ValueError(f"Produto com codigo {codigo} nao encontrado")
        consumidos = produto.baixar_estoque(quantidade)
        if produto.abaixo_do_minimo():
            print(f"[ALERTA] Estoque de '{produto.nome}' abaixo do minimo "
                  f"({produto.quantidade_total()}/{produto.estoque_minimo})")
        return consumidos

    def descartar_vencidos_geral(self, data_atual):
        """Roda o descarte de vencidos em todos os produtos."""
        for produto in self.produtos.percorrer():
            produto.descartar_vencidos(data_atual)

    def produtos_abaixo_do_minimo(self):
        resultado = Lista()
        for produto in self.produtos.percorrer():
            if produto.abaixo_do_minimo():
                resultado.inserir(produto)
        return resultado


if __name__ == "__main__":
    # Teste rapido manual
    controle = ControleEstoque()

    pastilha = Produto("Pastilha de freio dianteira", "PST001", "Fornecedor A",
                        preco_venda=120.0, estoque_minimo=5)
    controle.cadastrar_produto(pastilha)

    controle.adicionar_lote("PST001", Lote(data_compra="2026-09-01", preco_compra=60.0, quantidade=10))
    controle.adicionar_lote("PST001", Lote(data_compra="2026-10-01", preco_compra=65.0, quantidade=8))

    print("Estoque total de pastilhas:", pastilha.quantidade_total())

    consumidos = controle.baixar_estoque("PST001", 12)
    print("Lotes consumidos na baixa de 12 unidades:")
    for lote in consumidos.percorrer():
        print(" ->", lote)

    print("Estoque restante:", pastilha.quantidade_total())
    print("Lotes restantes na fila:", list(pastilha.lotes.percorrer()))
