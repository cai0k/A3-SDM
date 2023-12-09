from sqlite3 import Cursor
from cliente import GerenciadorClientes
from estoque import GerenciadorEstoque
from database import conectar_banco, criar_tabelas, adicionar_cliente, selecionar_cliente, update_cliente, excluir_cliente, adicionar_produto, listar_produtos, buscar_produto, atualizar_produto, excluir_produto, realizar_venda, preencher_tabelas, produtos_mais_vendidos, produtos_por_cliente, consumo_medio_cliente, produtos_baixo_estoque
from database import conectar_banco

connection = conectar_banco()
criar_tabelas()
preencher_tabelas()
gerenciador_clientes = GerenciadorClientes()
gerenciador_estoque = GerenciadorEstoque()

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
            print(f"Cliente cadastrado com sucesso.")

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

connection.close()