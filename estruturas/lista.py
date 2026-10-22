"""
Estrutura de dados genérica: Lista Encadeada.

Implementação própria, sem uso de list() do Python para armazenar os
elementos. Pode ser usada como bloco de construção por qualquer módulo
de regra de negócio (clientes, veiculos, pecas em OS, etc.).
"""


class _NoLista:
    """Nó interno da lista encadeada. Uso exclusivo da classe Lista."""

    def __init__(self, valor):
        self.valor = valor
        self.proximo = None


class Lista:
    """
    Lista encadeada simples, genérica.

    Metodos:
        inserir(valor): insere no final da lista
        remover(valor, chave=None): remove o primeiro elemento que
            satisfaça a comparação (ver 'chave')
        buscar(valor, chave=None): retorna o elemento encontrado ou None
        percorrer(): gera cada valor armazenado, em ordem
        tamanho(): quantidade de elementos
        esta_vazia(): True/False
    """

    def __init__(self):
        self._cabeca = None
        self._tamanho = 0

    def esta_vazia(self):
        return self._cabeca is None

    def tamanho(self):
        return self._tamanho

    def inserir(self, valor):
        """Insere um novo valor no final da lista. O(n)."""
        novo_no = _NoLista(valor)
        if self._cabeca is None:
            self._cabeca = novo_no
        else:
            atual = self._cabeca
            while atual.proximo is not None:
                atual = atual.proximo
            atual.proximo = novo_no
        self._tamanho += 1

    def remover(self, criterio):
        """
        Remove o primeiro elemento para o qual criterio(valor) seja True.
        criterio: função que recebe um valor da lista e retorna bool.
        Retorna o valor removido, ou None se não encontrado.
        """
        anterior = None
        atual = self._cabeca
        while atual is not None:
            if criterio(atual.valor):
                if anterior is None:
                    self._cabeca = atual.proximo
                else:
                    anterior.proximo = atual.proximo
                self._tamanho -= 1
                return atual.valor
            anterior = atual
            atual = atual.proximo
        return None

    def buscar(self, criterio):
        """
        Retorna o primeiro valor para o qual criterio(valor) seja True.
        criterio: função que recebe um valor da lista e retorna bool.
        """
        atual = self._cabeca
        while atual is not None:
            if criterio(atual.valor):
                return atual.valor
            atual = atual.proximo
        return None

    def percorrer(self):
        """Gerador: percorre todos os valores em ordem de inserção."""
        atual = self._cabeca
        while atual is not None:
            yield atual.valor
            atual = atual.proximo

    def __iter__(self):
        return self.percorrer()

    def __len__(self):
        return self._tamanho
