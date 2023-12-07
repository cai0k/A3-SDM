class Produto:
    def __init__(self, codigo, nome, preco, estoque):
        self.codigo = codigo
        self.nome = nome
        self.preco = preco
        self.estoque = estoque


class GerenciadorEstoque:
    def __init__(self):
        self.produtos = []

    def adicionar_produto(self, codigo, nome, preco, estoque):
        produto = Produto(codigo, nome, preco, estoque)
        self.produtos.append(produto)
        print(f"Produto {nome} adicionado ao estoque com sucesso.")

    def listar_produtos(self):
        print("\nLista de Produtos:")
        for produto in self.produtos:
            print(f"{produto.codigo} - {produto.nome} - Preço: {produto.preco} - estoque: {produto.estoque}")

    def buscar_produto(self, codigo):
        for produto in self.produtos:
            if produto.codigo == codigo:
                return produto
        return None

    def atualizar_produto(self, codigo, novo_preco, novo_estoque):
        produto = self.buscar_produto(codigo)
        if produto:
            produto.preco = novo_preco
            produto.estoque = novo_estoque
            print(f"Dados do produto {codigo} atualizados: Preço: {novo_preco}, estoque: {novo_estoque}.")
        else:
            print(f"Produto não encontrado.")

    def atualizar_cliente(self, nome, novo_email):
        cliente = self.buscar_cliente(nome)
        if cliente:
            cliente.email = novo_email
            print(f"Email do cliente {nome} atualizado para {novo_email}.")
        else:
            print(f"Cliente {nome} não encontrado.")       

    def excluir_produto(self, codigo):
        produto = self.buscar_produto(codigo)
        if produto:
            self.produtos.remove(produto)
            print(f"Produto {produto.nome} excluído do estoque com sucesso.")
        else:
            print("Produto não encontrado.")
