from database import adicionar_cliente, excluir_cliente, selecionar_cliente, update_cliente


class Cliente:
    def __init__(self, nome, email):
        self.nome = nome
        self.email = email


class GerenciadorClientes:
    def __init__(self):
        self.clientes = []
        self.proximo_id = 1

    def adicionar_cliente(self, nome, email, cursor):
        cliente = Cliente(nome, email)
        self.clientes.append(cliente)

        adicionar_cliente(nome, email, cursor)

    def selecionar_cliente(self, cliente_id, cursor):
        return selecionar_cliente(cliente_id, cursor)

    def update_cliente(self, cliente_id, novo_nome, novo_email, cursor):
        update_cliente(cliente_id, novo_nome, novo_email, cursor)

    def excluir_cliente(self, cliente_id, cursor):
        excluir_cliente(cliente_id, cursor)