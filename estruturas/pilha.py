"""
Estrutura de dados genérica: Pilha (LIFO).

Implementação própria com nós encadeados. Pode ser útil, por exemplo,
para histórico de ações sobre uma OS (desfazer inclusão de peça/serviço)
ou para pilha de chamadas no percurso da árvore de componentes.
"""


class _NoPilha:
    """Nó interno da pilha. Uso exclusivo da classe Pilha."""

    def __init__(self, valor):
        self.valor = valor
        self.anterior = None


class Pilha:
    """
    Pilha genérica (LIFO - Last In, First Out).

    Metodos:
        empilhar(valor): insere no topo
        desempilhar(): remove e retorna o elemento do topo
        topo(): retorna o elemento do topo sem remover
        esta_vazia(): True/False
        tamanho(): quantidade de elementos
    """

    def __init__(self):
        self._topo = None
        self._tamanho = 0

    def esta_vazia(self):
        return self._topo is None

    def tamanho(self):
        return self._tamanho

    def empilhar(self, valor):
        """Insere um valor no topo da pilha. O(1)."""
        novo_no = _NoPilha(valor)
        novo_no.anterior = self._topo
        self._topo = novo_no
        self._tamanho += 1

    def desempilhar(self):
        """Remove e retorna o valor do topo da pilha. O(1)."""
        if self._topo is None:
            return None
        no_removido = self._topo
        self._topo = self._topo.anterior
        self._tamanho -= 1
        return no_removido.valor

    def topo(self):
        """Retorna o valor do topo sem remover."""
        if self._topo is None:
            return None
        return self._topo.valor

    def __len__(self):
        return self._tamanho
