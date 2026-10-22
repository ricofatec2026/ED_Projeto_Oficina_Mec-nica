"""
Testes manuais simples das estruturas genericas.
Rodar com: python -m testes.teste_estruturas (a partir da raiz do projeto)
"""

from estruturas.lista import Lista
from estruturas.fila import Fila
from estruturas.pilha import Pilha
from estruturas.arvore import NoArvore, ArvoreComponentes


def testar_lista():
    print("== Lista ==")
    lista = Lista()
    lista.inserir("A")
    lista.inserir("B")
    lista.inserir("C")
    print("Conteudo:", list(lista.percorrer()))
    removido = lista.remover(lambda v: v == "B")
    print("Removido:", removido, "| Conteudo apos remover:", list(lista.percorrer()))
    print("Tamanho:", lista.tamanho())


def testar_fila():
    print("\n== Fila ==")
    fila = Fila()
    fila.enfileirar(1)
    fila.enfileirar(2)
    fila.enfileirar(3)
    print("Frente:", fila.espiar())
    print("Desenfileirado:", fila.desenfileirar())
    print("Conteudo restante:", list(fila.percorrer()))


def testar_pilha():
    print("\n== Pilha ==")
    pilha = Pilha()
    pilha.empilhar("x")
    pilha.empilhar("y")
    print("Topo:", pilha.topo())
    print("Desempilhado:", pilha.desempilhar())
    print("Topo apos desempilhar:", pilha.topo())


def testar_arvore():
    print("\n== Arvore de Componentes ==")
    veiculo = NoArvore("Veiculo")
    motor = NoArvore("Motor")
    ignicao = NoArvore("Sistema de ignicao")
    vela = NoArvore("Vela", codigo_peca="VLA001", estado="OK")
    ignicao.adicionar_filho(vela)
    motor.adicionar_filho(ignicao)
    veiculo.adicionar_filho(motor)

    freios = NoArvore("Freios")
    pastilha = NoArvore("Pastilha dianteira", codigo_peca="PST001", estado="OK")
    freios.adicionar_filho(pastilha)
    veiculo.adicionar_filho(freios)

    arvore = ArvoreComponentes(veiculo)
    arvore.exibir_indentada()

    arvore.marcar_estado("PST001", "Com defeito")
    print("\nApos marcar pastilha com defeito:")
    arvore.exibir_indentada()


if __name__ == "__main__":
    testar_lista()
    testar_fila()
    testar_pilha()
    testar_arvore()
