class Cliente:
    def __init__(self, nome, email):
        self.nome = nome
        self.email = email


class GerenciadorClientes:
    def __init__(self):
        self.clientes = []

    def adicionar_cliente(self, nome, email):
        cliente = Cliente(nome, email)
        self.clientes.append(cliente)
        print(f"Cliente {nome} adicionado com sucesso.")

    def listar_clientes(self):
        print("\nLista de Clientes:")
        for cliente in self.clientes:
            print(f"{cliente.nome} - {cliente.email}")

    def buscar_cliente(self, nome):
        for cliente in self.clientes:
            if cliente.nome == nome:
                return cliente
        return None

    def atualizar_cliente(self, nome, novo_email):
        cliente = self.buscar_cliente(nome)
        if cliente:
            cliente.email = novo_email
            print(f"Email do cliente {nome} atualizado para {novo_email}.")
        else:
            print(f"Cliente {nome} não encontrado.")

    def excluir_cliente(self, nome):
        cliente = self.buscar_cliente(nome)
        if cliente:
            self.clientes.remove(cliente)
            print(f"Cliente {nome} excluído com sucesso.")
        else:
            print(f"Cliente {nome} não encontrado.")