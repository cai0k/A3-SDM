from flask import Flask, jsonify, request
from cliente import GerenciadorClientes
from estoque import GerenciadorEstoque
from database import (
    conectar_banco,
    criar_tabelas,
    adicionar_produto,
    listar_produtos,
    atualizar_produto,
    excluir_produto,
    realizar_venda,
    preencher_tabelas,
    produtos_mais_vendidos,
    produtos_por_cliente,
    consumo_medio_cliente,
    produtos_baixo_estoque,
    adicionar_cliente,  
    selecionar_cliente,  
    update_cliente,  
    excluir_cliente,  
)
from database import conectar_banco

app = Flask(__name__)
connection = conectar_banco()
criar_tabelas()
preencher_tabelas()
gerenciador_clientes = GerenciadorClientes()
gerenciador_estoque = GerenciadorEstoque()

def interacao_terminal():
    while True:
        print("\nOpções:")
        print("1. Gerenciar Clientes")
        print("2. Gerenciar Estoque")
        print("3. Relatórios")
        print("4. Sair")

        opcao = input("Escolha uma opção (1-4): ")

        if opcao == '1':
            print("\nOpções de Cliente:")
            print("1. Adicionar Cliente")
            print("2. Listar Clientes")
            print("3. Atualizar Cliente")
            print("4. Excluir Cliente")
            print("5. Comprar")
            print("6. Voltar")

            opcao_cliente = input("Escolha uma opção (1-6): ")

            if opcao_cliente == '1':
                nome = input("Digite o nome do cliente: ")
                email = input("Digite o email do cliente: ")
                adicionar_cliente(nome, email)
                print(f"Cliente cadastrado com susso.")

            elif opcao_cliente == '2':
                id = int(input("Digite o id do cliente: "))
                cliente = selecionar_cliente(id)
                if cliente:
                    print(f"Cliente encontrado: {cliente}")
                else:
                    print("Cliente não encontrado.")

            elif opcao_cliente == '3':
                nome = input("Digite o nome do cliente que deseja atualizar: ")
                novo_nome = input("Digite o novo nome: ")
                novo_email = input("Digite o novo email: ")
                update_cliente(nome, novo_nome, novo_email)
                print(f"Dados do cliente atualizados com sucesso.")

            elif opcao_cliente == '4':
                id = input("Digite o nome do cliente que deseja excluir: ")
                excluir_cliente(id)
                print(f"Cliente excluído com sucesso.")

            elif opcao_cliente == '5':
                cliente_nome = input("Digite o nome do cliente: ")
                cliente = gerenciador_clientes.buscar_cliente(cliente_nome)

                if cliente:
                    gerenciador_estoque.listar_produtos()
                    codigo_produto = int(input("Digite o código do produto que deseja comprar: "))
                    quantidade_compra = int(input("Digite a quantidade que deseja comprar: "))

                    sucesso = realizar_venda(cliente.id, codigo_produto, quantidade_compra)

                    if sucesso:
                        print(f"Compra realizada com sucesso para o cliente {cliente.nome}.")
                    else:
                        print("A compra não pôde ser concluída devido ao estoque insuficiente.")

            elif opcao_cliente == '6':
                pass

            else:
                print("Opção inválida. Tente novamente.")

        elif opcao == '2':
            print("\nOpções de Estoque:")
            print("1. Adicionar Produto")
            print("2. Listar Produtos")
            print("3. Atualizar Produto")
            print("4. Excluir Produto")
            print("5. Voltar")

            opcao_estoque = input("Escolha uma opção (1-5): ")

            if opcao_estoque == '1':
                codigo = int(input("Digite o código do produto: "))
                nome_produto = input("Digite o nome do produto: ")
                preco = float(input("Digite o preço do produto: "))
                estoque = int(input("Digite a quantidade dos produtos: "))
                adicionar_produto(codigo, nome_produto, preco, estoque)
                print(f"Produto {nome_produto} adicionado ao estoque com sucesso.")

            elif opcao_estoque == '2':
                produtos = listar_produtos()
                print("\nLista de Produtos:")
                for produto in produtos:
                    print(f"{produto[0]} - {produto[1]} - Preço: {produto[2]} - Estoque: {produto[3]}")

            elif opcao_estoque == '3':
                codigo = int(input("Digite o código do produto: "))
                novo_preco = float(input("Digite o novo preço: "))
                novo_estoque = int(input("Digite a nova quantidade: "))
                atualizar_produto(codigo, novo_preco, novo_estoque)
                print(f"Dados do produto {codigo} atualizados com sucesso.")

            elif opcao_estoque == '4':
                codigo = int(input("Digite o código do produto que deseja excluir: "))
                excluir_produto(codigo)
                print(f"Produto {codigo} excluído do estoque com sucesso.")

            elif opcao_estoque == '6':
                pass
        

        elif opcao == '3':
            print("\nOpções de Relatórios:")
            print("1. Produtos Mais Vendidos")
            print("2. Produtos por Cliente")
            print("3. Consumo Médio do Cliente")
            print("4. Produtos com Baixo Estoque")
            print("5. Voltar")

            opcao_relatorio = input("Escolha uma opção (1-5): ")

            if opcao_relatorio == '1':
                relatorio = produtos_mais_vendidos(connection.cursor())
                print("\nProdutos Mais Vendidos:")
                for produto, quantidade in relatorio:
                    print(f"{produto} - Quantidade Vendida: {quantidade}")

            elif opcao_relatorio == '2':
                cliente_id = int(input("Digite o ID do cliente: "))
                relatorio = produtos_por_cliente(connection.cursor(), cliente_id)
                print("\nProdutos por Cliente:")
                for produto, quantidade in relatorio:
                    print(f"{produto} - Quantidade Comprada: {quantidade}")

            elif opcao_relatorio == '3':
                cliente_id = int(input("Digite o ID do cliente: "))
                consumo_medio = consumo_medio_cliente(connection.cursor(), cliente_id)
                print(f"\nConsumo Médio do Cliente: {consumo_medio:.2f}")

            elif opcao_relatorio == '4':
                limite_estoque = int(input("Digite o limite de estoque: "))
                relatorio = produtos_baixo_estoque(connection.cursor(), limite_estoque)
                print("\nProdutos com Baixo Estoque:")
                for produto, estoque in relatorio:
                    print(f"{produto} - Estoque: {estoque}")

            elif opcao_relatorio == '5':
                pass

        elif opcao == '4':
            print("Saindo...")
            break

def realizar_venda_terminal():
    cliente_nome = input("Digite o nome do cliente: ")
    cliente = gerenciador_clientes.buscar_cliente(cliente_nome)

    if cliente:
        gerenciador_estoque.listar_produtos()
        codigo_produto = int(input("Digite o código do produto que deseja comprar: "))
        quantidade_compra = int(input("Digite a quantidade que deseja comprar: "))

        sucesso = realizar_venda(cliente.id, codigo_produto, quantidade_compra)

        if sucesso:
            print(f"Compra realizada com sucesso para o cliente {cliente.nome}.")
        else:
            print("A compra não pôde ser concluída devido ao estoque insuficiente.")
    else:
        print("Cliente não encontrado.")

    connection.close()


# @app.route('/realizar_venda', methods=['POST'])
# def realizar_venda_api():
#     data = request.get_json()

#     cliente_nome = data.get('cliente_nome')
#     codigo_produto = data.get('codigo_produto')
#     quantidade_compra = data.get('quantidade_compra')

#     cliente = gerenciador_clientes.buscar_cliente(cliente_nome)

#     if cliente:
#         sucesso = realizar_venda(cliente.id, codigo_produto, quantidade_compra)

#         if sucesso:
#             return jsonify({"mensagem": f"Compra realizada com sucesso para o cliente {cliente.nome}."}), 200
#         else:
#             return jsonify({"mensagem": "A compra não pôde ser concluída devido ao estoque insuficiente."}), 400
#     else:
#         return jsonify({"mensagem": "Cliente não encontrado."}), 404

@app.route('/clientes', methods=['GET'])
def get_clientes():
    clientes = gerenciador_clientes.listar_clientes()
    return jsonify(clientes)

@app.route('/clientes/<int:cliente_id>', methods=['GET'])
def get_cliente(cliente_id):
    cliente = gerenciador_clientes.selecionar_cliente(cliente_id)
    if cliente:
        return jsonify(cliente)
    else:
        return jsonify({"mensagem": "Cliente não encontrado"}), 404

@app.route('/clientes', methods=['POST'])
def adicionar_cliente_api():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')

    with connection.cursor() as cursor:
        gerenciador_clientes.adicionar_cliente(nome, email, cursor)

        connection.commit()
    return jsonify({"mensagem": "Cliente adicionado com sucesso"}), 201

@app.route('/clientes/<int:cliente_id>', methods=['PUT'])
def atualizar_cliente_api(cliente_id):
    data = request.get_json()
    novo_nome = data.get('novo_nome')
    novo_email = data.get('novo_email')

    update_cliente(cliente_id, novo_nome, novo_email)
    return jsonify({"mensagem": "Cliente atualizado com sucesso"})

@app.route('/clientes/<int:cliente_id>', methods=['DELETE'])
def excluir_cliente_api(cliente_id):
    excluir_cliente(cliente_id)
    return jsonify({"mensagem": "Cliente excluído com sucesso"})

@app.route('/estoque', methods=['GET'])
def get_estoque_api():
    produtos = listar_produtos()
    return jsonify(produtos)

@app.route('/estoque/<int:produto_id>', methods=['GET'])
def get_produto_api(produto_id):
    produto = buscar_produto(produto_id)
    if produto:
        return jsonify(produto)
    else:
        return jsonify({"mensagem": "Produto não encontrado"}), 404

@app.route('/estoque', methods=['POST'])
def adicionar_produto_api():
    data = request.get_json()
    codigo = data.get('codigo')
    nome_produto = data.get('nome_produto')
    preco = data.get('preco')
    estoque = data.get('estoque')

    adicionar_produto(codigo, nome_produto, preco, estoque)
    return jsonify({"mensagem": "Produto adicionado ao estoque com sucesso"}), 201

@app.route('/estoque/<int:produto_id>', methods=['PUT'])
def atualizar_produto_api(produto_id):
    data = request.get_json()
    novo_preco = data.get('novo_preco')
    novo_estoque = data.get('novo_estoque')

    atualizar_produto(produto_id, novo_preco, novo_estoque)
    return jsonify({"mensagem": "Produto atualizado com sucesso"})

@app.route('/estoque/<int:produto_id>', methods=['DELETE'])
def excluir_produto_api(produto_id):
    excluir_produto(produto_id)
    return jsonify({"mensagem": "Produto excluído do estoque com sucesso"})


if __name__ == '__main__':
    import threading
    terminal_thread = threading.Thread(target=interacao_terminal)
    terminal_thread.start()

    app.run(debug=True)       
