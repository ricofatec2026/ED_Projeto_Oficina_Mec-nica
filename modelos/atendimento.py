"""
Regra de negocio: Controle de Atendimento (fila de espera dos veiculos).

Combinacao de estruturas (documentar no README):
    Fila (guincho) + Fila (normal)
    -> o proximo veiculo chamado vem da fila de guincho, se nao estiver
       vazia; senao, vem da fila normal.
"""

from estruturas.fila import Fila


class VeiculoEspera:
    """Representa um veiculo aguardando atendimento."""

    def __init__(self, placa, nome_cliente, data_hora_chegada, queixa, guincho=False):
        self.placa = placa
        self.nome_cliente = nome_cliente
        self.data_hora_chegada = data_hora_chegada
        self.queixa = queixa
        self.guincho = guincho

    def __repr__(self):
        tag = "[GUINCHO] " if self.guincho else ""
        return f"{tag}{self.placa} - {self.nome_cliente} ({self.queixa})"


class ControleAtendimento:
    """
    Gerencia a fila de espera de veiculos, com prioridade para guincho.

    Duas filas proprias trabalhando juntas (combinacao de estruturas):
    - fila_guincho: veiculos trazidos por guincho
    - fila_normal: demais veiculos
    """

    def __init__(self):
        self.fila_guincho = Fila()
        self.fila_normal = Fila()

    def chegar_veiculo(self, veiculo: VeiculoEspera):
        """Adiciona um veiculo na fila correta, conforme guincho ou nao."""
        if veiculo.guincho:
            self.fila_guincho.enfileirar(veiculo)
        else:
            self.fila_normal.enfileirar(veiculo)

    def proximo_veiculo(self):
        """
        Quando um box fica livre: retorna o proximo veiculo a ser
        atendido. Prioridade para a fila de guincho; se vazia, usa a
        fila normal.
        """
        if not self.fila_guincho.esta_vazia():
            return self.fila_guincho.desenfileirar()
        return self.fila_normal.desenfileirar()

    def esta_vazia(self):
        return self.fila_guincho.esta_vazia() and self.fila_normal.esta_vazia()


if __name__ == "__main__":
    # Teste rapido manual (sera substituido por testes formais depois)
    controle = ControleAtendimento()
    controle.chegar_veiculo(VeiculoEspera("ABC1234", "Joao", "22/10 08:00", "Barulho no freio"))
    controle.chegar_veiculo(VeiculoEspera("XYZ9999", "Maria", "22/10 08:05", "Motor falhando", guincho=True))
    controle.chegar_veiculo(VeiculoEspera("QWE4321", "Pedro", "22/10 08:10", "Nao liga"))

    print("Chamando veiculos na ordem correta (guincho primeiro):")
    while not controle.esta_vazia():
        print(" ->", controle.proximo_veiculo())
