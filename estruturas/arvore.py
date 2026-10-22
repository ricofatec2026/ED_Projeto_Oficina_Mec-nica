"""
Estrutura de dados genérica: Árvore N-ária.

ATENÇÃO (restrição do enunciado): esta árvore NÃO é binária e NÃO é uma
árvore de busca. Cada nó pode ter de 0 a N filhos. É usada para
representar a hierarquia de componentes do veículo:
    Veículo -> Sistemas -> Subconjuntos -> Peças
"""


class NoArvore:
    """
    Nó da árvore de componentes.

    Atributos:
        nome: nome do componente (ex.: "Motor", "Vela")
        codigo_peca: código da peça, quando o nó representa uma peça
            (None para nós que são apenas agrupadores, como "Motor")
        estado: "OK" ou "Com defeito" (relevante para nós-folha/peça)
        filhos: Lista (estrutura própria) de NoArvore
    """

    def __init__(self, nome, codigo_peca=None, estado="OK"):
        from estruturas.lista import Lista

        self.nome = nome
        self.codigo_peca = codigo_peca
        self.estado = estado
        self.filhos = Lista()

    def adicionar_filho(self, no_filho):
        self.filhos.inserir(no_filho)

    def eh_folha(self):
        return self.filhos.esta_vazia()


class ArvoreComponentes:
    """
    Árvore de componentes do veículo.

    Metodos:
        exibir_indentada(): imprime a árvore em pré-ordem, com indentação
        buscar_por_codigo(codigo): busca um nó-peça pelo código
        marcar_estado(codigo, novo_estado): marca uma peça como
            "OK" ou "Com defeito" durante o diagnóstico
    """

    def __init__(self, raiz: NoArvore):
        self.raiz = raiz

    def exibir_indentada(self, no=None, nivel=0):
        """Percurso em profundidade (pré-ordem), exibindo indentado."""
        if no is None:
            no = self.raiz

        prefixo = "  " * nivel + "- "
        info_peca = f" [{no.codigo_peca} | {no.estado}]" if no.codigo_peca else ""
        print(f"{prefixo}{no.nome}{info_peca}")

        for filho in no.filhos.percorrer():
            self.exibir_indentada(filho, nivel + 1)

    def buscar_por_codigo(self, codigo, no=None):
        """Busca em profundidade um nó-peça pelo código. Retorna o NoArvore ou None."""
        if no is None:
            no = self.raiz

        if no.codigo_peca == codigo:
            return no

        for filho in no.filhos.percorrer():
            encontrado = self.buscar_por_codigo(codigo, filho)
            if encontrado is not None:
                return encontrado
        return None

    def marcar_estado(self, codigo, novo_estado):
        """Marca o estado (OK / Com defeito) de uma peça pelo código."""
        no = self.buscar_por_codigo(codigo)
        if no is not None:
            no.estado = novo_estado
            return True
        return False
