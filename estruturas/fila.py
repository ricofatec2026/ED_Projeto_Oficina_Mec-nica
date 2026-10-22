"""
Estrutura de dados genérica: Fila (FIFO).

Implementação própria com nós encadeados. Usada, por exemplo, para:
- fila de espera de atendimento (normal e guincho)
- fila de lotes de estoque (consumo do mais antigo primeiro)
"""


class _NoFila:
    """Nó interno da fila. Uso exclusivo da classe Fila."""

    def __init__(self, valor):
        self.valor = valor
        self.proximo = None


class Fila:
    """
    Fila genérica (FIFO - First In, First Out).

    Metodos:
        enfileirar(valor): insere no final da fila
        desenfileirar(): remove e retorna o elemento da frente
        espiar(): retorna o elemento da frente sem remover
        esta_vazia(): True/False
        tamanho(): quantidade de elementos
    """

    def __init__(self):
        self._frente = None
        self._fim = None
        self._tamanho = 0

    def esta_vazia(self):
        return self._frente is None

    def tamanho(self):
        return self._tamanho

    def enfileirar(self, valor):
        """Insere um valor no fim da fila. O(1)."""
        novo_no = _NoFila(valor)
        if self._fim is None:
            self._frente = novo_no
            self._fim = novo_no
        else:
            self._fim.proximo = novo_no
            self._fim = novo_no
        self._tamanho += 1

    def desenfileirar(self):
        """Remove e retorna o valor da frente da fila. O(1)."""
        if self._frente is None:
            return None
        no_removido = self._frente
        self._frente = self._frente.proximo
        if self._frente is None:
            self._fim = None
        self._tamanho -= 1
        return no_removido.valor

    def espiar(self):
        """Retorna o valor da frente sem remover."""
        if self._frente is None:
            return None
        return self._frente.valor

    def percorrer(self):
        """Gerador: percorre os valores da frente para o fim, sem remover."""
        atual = self._frente
        while atual is not None:
            yield atual.valor
            atual = atual.proximo

    def __iter__(self):
        return self.percorrer()

    def __len__(self):
        return self._tamanho
