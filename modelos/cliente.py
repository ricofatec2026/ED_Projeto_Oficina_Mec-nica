"""
Regra de negocio: Controle de Clientes e Veiculos.

Combinacao de estruturas (documentar no README):
    Lista (clientes) + Lista (veiculos de cada cliente)
    -> cada Cliente guarda uma Lista propria de Veiculo.
       Buscar um veiculo pela placa percorre a lista de clientes e,
       para cada um, a lista de veiculos.
"""

from estruturas.lista import Lista


class Veiculo:
    """Representa um veiculo cadastrado na oficina."""

    def __init__(self, placa, modelo, marca, ano):
        self.placa = placa
        self.modelo = modelo
        self.marca = marca
        self.ano = ano

    def __repr__(self):
        return f"{self.placa} - {self.marca} {self.modelo} ({self.ano})"


class Cliente:
    """
    Representa um cliente da oficina.

    Cada cliente possui sua propria Lista de veiculos, que pode crescer
    sem limite pre-definido ao longo do tempo.
    """

    def __init__(self, nome, cpf, telefone):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.veiculos = Lista()

    def adicionar_veiculo(self, veiculo: Veiculo):
        self.veiculos.inserir(veiculo)

    def remover_veiculo(self, placa):
        """Remove um veiculo deste cliente pela placa. Retorna o veiculo removido ou None."""
        return self.veiculos.remover(lambda v: v.placa == placa)

    def buscar_veiculo(self, placa):
        """Busca um veiculo deste cliente pela placa."""
        return self.veiculos.buscar(lambda v: v.placa == placa)

    def __repr__(self):
        return f"{self.nome} (CPF: {self.cpf}) - {len(self.veiculos)} veiculo(s)"


class ControleClientes:
    """
    Gerencia a Lista de clientes da oficina.

    Metodos:
        cadastrar_cliente(cliente)
        buscar_cliente_por_cpf(cpf)
        remover_cliente(cpf)
        cadastrar_veiculo(cpf, veiculo)
        buscar_veiculo_por_placa(placa) -> percorre todos os clientes
        remover_veiculo_por_placa(placa)
    """

    def __init__(self):
        self.clientes = Lista()

    # --- Clientes ---

    def cadastrar_cliente(self, cliente: Cliente):
        if self.buscar_cliente_por_cpf(cliente.cpf) is not None:
            raise ValueError(f"Ja existe cliente cadastrado com CPF {cliente.cpf}")
        self.clientes.inserir(cliente)

    def buscar_cliente_por_cpf(self, cpf):
        return self.clientes.buscar(lambda c: c.cpf == cpf)

    def remover_cliente(self, cpf):
        """Remove um cliente (e, com ele, seus veiculos) pelo CPF."""
        return self.clientes.remover(lambda c: c.cpf == cpf)

    # --- Veiculos (combinacao Lista + Lista) ---

    def cadastrar_veiculo(self, cpf, veiculo: Veiculo):
        """Adiciona um veiculo a um cliente ja cadastrado, buscando-o pelo CPF."""
        cliente = self.buscar_cliente_por_cpf(cpf)
        if cliente is None:
            raise ValueError(f"Cliente com CPF {cpf} nao encontrado")
        cliente.adicionar_veiculo(veiculo)

    def buscar_veiculo_por_placa(self, placa):
        """
        Percorre a lista de clientes e, para cada um, sua lista de
        veiculos, ate encontrar a placa buscada.
        Retorna uma tupla (cliente, veiculo) ou (None, None).
        """
        for cliente in self.clientes.percorrer():
            veiculo = cliente.buscar_veiculo(placa)
            if veiculo is not None:
                return cliente, veiculo
        return None, None

    def remover_veiculo_por_placa(self, placa):
        """Localiza o cliente dono da placa e remove o veiculo dele."""
        cliente, veiculo = self.buscar_veiculo_por_placa(placa)
        if cliente is None:
            return None
        return cliente.remover_veiculo(placa)


if __name__ == "__main__":
    # Teste rapido manual
    controle = ControleClientes()

    joao = Cliente("Joao Silva", "111.111.111-11", "19999990000")
    controle.cadastrar_cliente(joao)
    controle.cadastrar_veiculo("111.111.111-11", Veiculo("ABC1234", "Onix", "Chevrolet", 2020))
    controle.cadastrar_veiculo("111.111.111-11", Veiculo("XYZ9999", "HB20", "Hyundai", 2019))

    maria = Cliente("Maria Souza", "222.222.222-22", "19988887777")
    controle.cadastrar_cliente(maria)
    controle.cadastrar_veiculo("222.222.222-22", Veiculo("QWE4321", "Civic", "Honda", 2021))

    print("Busca por CPF:", controle.buscar_cliente_por_cpf("111.111.111-11"))

    cliente, veiculo = controle.buscar_veiculo_por_placa("XYZ9999")
    print("Busca por placa XYZ9999:", veiculo, "| dono:", cliente.nome)

    removido = controle.remover_veiculo_por_placa("ABC1234")
    print("Veiculo removido:", removido)
    print("Veiculos restantes de Joao:", list(joao.veiculos.percorrer()))
