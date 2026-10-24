"""
Regra de negocio: Diagnostico (Arvore de Componentes).

O enunciado pede uma arvore PRE-DEFINIDA (nao precisa ser editavel em
estrutura, apenas usada para marcar o estado das pecas durante o
diagnostico). Usa a estrutura generica ArvoreComponentes / NoArvore
(estruturas/arvore.py), que ja garante: arvore N-aria (0 a N filhos),
nao binaria, nao de busca.

Hierarquia conforme o exemplo do enunciado:
    Veiculo
      Motor
        Sistema de ignicao
          Vela
          Bobina
        Correia dentada
      Freios
        Pastilha dianteira
        Disco dianteiro
      Suspensao
        Amortecedor
        Bandeja
"""

from estruturas.arvore import NoArvore, ArvoreComponentes


def montar_arvore_padrao():
    """
    Monta e retorna a ArvoreComponentes pre-definida do veiculo, com os
    codigos de peca atribuidos as folhas (os nos agrupadores, como
    "Motor" ou "Sistema de ignicao", nao tem codigo_peca).
    """
    veiculo = NoArvore("Veiculo")

    # --- Motor ---
    motor = NoArvore("Motor")

    sistema_ignicao = NoArvore("Sistema de ignicao")
    sistema_ignicao.adicionar_filho(NoArvore("Vela", codigo_peca="VLA001"))
    sistema_ignicao.adicionar_filho(NoArvore("Bobina", codigo_peca="BOB001"))
    motor.adicionar_filho(sistema_ignicao)

    motor.adicionar_filho(NoArvore("Correia dentada", codigo_peca="COR001"))

    veiculo.adicionar_filho(motor)

    # --- Freios ---
    freios = NoArvore("Freios")
    freios.adicionar_filho(NoArvore("Pastilha dianteira", codigo_peca="PST001"))
    freios.adicionar_filho(NoArvore("Disco dianteiro", codigo_peca="DSC001"))
    veiculo.adicionar_filho(freios)

    # --- Suspensao ---
    suspensao = NoArvore("Suspensao")
    suspensao.adicionar_filho(NoArvore("Amortecedor", codigo_peca="AMT001"))
    suspensao.adicionar_filho(NoArvore("Bandeja", codigo_peca="BDJ001"))
    veiculo.adicionar_filho(suspensao)

    return ArvoreComponentes(veiculo)


class ControleDiagnostico:
    """
    Fachada para o diagnostico de um veiculo durante o atendimento.

    Cada veiculo em diagnostico recebe sua propria copia da arvore
    padrao (cada atendimento tem seu proprio estado de pecas OK /
    Com defeito).
    """

    def __init__(self):
        self.arvore = montar_arvore_padrao()

    def exibir_diagnostico(self):
        """Exibe a arvore indentada, em pre-ordem (profundidade)."""
        self.arvore.exibir_indentada()

    def marcar_defeito(self, codigo_peca):
        """Marca uma peca como 'Com defeito' pelo codigo."""
        ok = self.arvore.marcar_estado(codigo_peca, "Com defeito")
        if not ok:
            raise ValueError(f"Peca com codigo {codigo_peca} nao encontrada na arvore")

    def marcar_ok(self, codigo_peca):
        """Marca uma peca como 'OK' pelo codigo."""
        ok = self.arvore.marcar_estado(codigo_peca, "OK")
        if not ok:
            raise ValueError(f"Peca com codigo {codigo_peca} nao encontrada na arvore")

    def listar_pecas_com_defeito(self, no=None, resultado=None):
        """
        Percorre a arvore (pre-ordem) e retorna uma Lista propria com
        os nos de peca marcados como 'Com defeito'. Util para alimentar
        a Ordem de Servico (dia 5).
        """
        from estruturas.lista import Lista

        if no is None:
            no = self.arvore.raiz
        if resultado is None:
            resultado = Lista()

        if no.codigo_peca is not None and no.estado == "Com defeito":
            resultado.inserir(no)

        for filho in no.filhos.percorrer():
            self.listar_pecas_com_defeito(filho, resultado)

        return resultado


if __name__ == "__main__":
    # Teste rapido manual
    diagnostico = ControleDiagnostico()

    print("Arvore de componentes (estado inicial):")
    diagnostico.exibir_diagnostico()

    diagnostico.marcar_defeito("PST001")  # Pastilha dianteira
    diagnostico.marcar_defeito("VLA001")  # Vela

    print("\nApos diagnostico do mecanico:")
    diagnostico.exibir_diagnostico()

    print("\nPecas com defeito encontradas:")
    for peca in diagnostico.listar_pecas_com_defeito().percorrer():
        print(" ->", peca.nome, peca.codigo_peca)
