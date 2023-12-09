import logging
import json
import requests


BASE_URL = "http://127.0.0.1:5000"


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
            
            response = requests.post(f"{BASE_URL}/cadastrarCliente", json={"nome": nome, "email": email})
            
            if response.status_code == 200:
                print("Cliente cadastrado com sucesso.")
            else:
                print("Erro ao cadastrar cliente.")

        elif opcao_cliente == '2':
            id_cliente = int(input("Digite o ID do cliente: "))
            response = requests.get(f"{BASE_URL}/buscarCliente/{id_cliente}")
    
            if response.status_code == 200:
                cliente = response.json()
                print(f"Cliente encontrado: {cliente}")
            else:
                print("Cliente não encontrado.")

        elif opcao_cliente == '3':
            nome = input("Digite o nome do cliente que deseja atualizar: ")
            novo_nome = input("Digite o novo nome: ")
            novo_email = input("Digite o novo email: ")
    
            response = requests.post(f"{BASE_URL}/editarCliente", json={"nome": nome, "novo_nome": novo_nome, "novo_email": novo_email})
    
            if response.status_code == 200:
                print("Dados do cliente atualizados com sucesso.")
            else:
                print("Erro ao atualizar cliente.")

        elif opcao_cliente == '4':
            id_cliente = input("Digite o ID do cliente que deseja excluir: ")
            response = requests.delete(f"{BASE_URL}/excluirCliente", json={"id": id_cliente})

            if response.status_code == 200:
                print("Cliente excluído com sucesso.")
            else:
                print("Erro ao excluir cliente.")

        elif opcao_cliente == '5':
            ClienteID = input("Digite o id do cliente: ")
            response_cliente = requests.get(f"{BASE_URL}/buscarCliente/{ClienteID}")

            if response_cliente.status_code == 200:
                cliente = response_cliente.json()
               
                if 'cliente' in cliente and len(cliente['cliente']) > 0:
                    cliente_id = cliente['cliente'][0]
                    codigo_produto = (input("Digite o id do produto que deseja comprar: "))
                    quantidade_compra = int(input("Digite a quantidade que deseja comprar: "))

                    dados_venda = {
                        "ClienteID": cliente_id,
                        "ProdutoID": codigo_produto,
                        "QuantidadeVendida": quantidade_compra
                    }
                    response_venda = requests.post(f"{BASE_URL}/realizarVenda",  json=dados_venda)

                    if response_venda.status_code == 200:
                        print("Venda realizada com sucesso.")
                        logging.info("Venda realizada com sucesso.")
                    else:
                        print("Erro ao realizar a venda. Motivo:", response_venda.json().get('error', ''))
                else:
                    print("Cliente não possui a chave 'id' no retorno da API.")
            else:
                print(f"Erro ao obter informações do cliente. Código: {response_cliente.status_code}")
                print("Resposta da API:", response_cliente.json())

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

            dados_produto = {
                'codigo': codigo,
                'nome': nome_produto,
                'preco': preco,
                'estoque': estoque
            }
            resposta = requests.post(f"{BASE_URL}/adicionarProduto", json=dados_produto)

            if resposta.status_code == 200:
                print("Produto adicionado com sucesso.")
            else:
                print("Falha ao adicionar produto.")

        elif opcao_estoque == '2':
            resposta = requests.get(f"{BASE_URL}/listarProdutos")
            if resposta.status_code == 200:
                produtos_json = resposta.json().get('produtos', [])

                if produtos_json:
                    print("\nLista de Produtos:")
                    for produto in produtos_json:
                        print(f"Código: {produto['codigo']} - Nome: {produto['nome']} - Preço: {produto['preco']} - Estoque: {produto['estoque']}")
                else:
                    print("A lista de produtos está vazia.")
            else:
                print("Erro ao obter a lista de produtos.")

        elif opcao_estoque == '3':
            codigo = int(input("Digite o código do produto: "))
            novo_preco = float(input("Digite o novo preço: "))
            novo_estoque = int(input("Digite a nova quantidade: "))
            dados_produto = {
                'codigo': codigo,
                'novo_preco': novo_preco,
                'novo_estoque': novo_estoque
            }

            resposta = requests.post(f"{BASE_URL}/atualizarProduto", json=dados_produto)

            if resposta.status_code == 200:
                print(f"Dados do produto {codigo} atualizados com sucesso.")
            else:
                print("Erro ao atualizar produto.")

        elif opcao_estoque == '4':
            codigo = int(input("Digite o código do produto que deseja excluir: "))

            dados_produto = {
                'codigo': codigo
            }
            resposta = requests.delete(f"{BASE_URL}/excluirProduto", json=dados_produto)

            if resposta.status_code == 200:
                print(f"Produto {codigo} excluído do estoque com sucesso.")
            else:
                print("Erro ao excluir produto.")

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
            resposta = requests.get(f"{BASE_URL}/produtosMaisVendidos")
            
            if resposta.status_code == 200:
                relatorio_json = resposta.json().get('produtos_mais_vendidos', [])

                if relatorio_json:
                    print("\nProdutos Mais Vendidos:")
                    for produto, quantidade in relatorio_json:
                        print(f"{produto} - Quantidade Vendida: {quantidade}")
                else:
                    print("O relatório de produtos mais vendidos está vazio.")
            else:
                print("Erro ao obter o relatório de produtos mais vendidos.")

        elif opcao_relatorio == '2':
            cliente_id = int(input("Digite o ID do cliente: "))
            resposta = requests.get(f"{BASE_URL}/produtos_por_cliente/{cliente_id}")

            if resposta.status_code == 200:
    
                relatorio_json = resposta.json()

                if relatorio_json:
                    print("\nProdutos por Cliente:")
                    for produto in relatorio_json:
                        print(f"{produto[0]} - Quantidade Comprada: {produto[1]}")
                else:
                    print("O relatório de produtos por cliente está vazio.")
            else:
                print("Erro ao obter o relatório de produtos por cliente.")

        elif opcao_relatorio == '3':
            cliente_id = int(input("Digite o ID do cliente: "))
            resposta = requests.get(f"{BASE_URL}/consumoMedioCliente/{cliente_id}")

            if resposta.status_code == 200:
                resultado_json = resposta.json()

                if 'consumo_medio_cliente' in resultado_json:
                    consumo_medio = resultado_json['consumo_medio_cliente']
                    print(f"\nConsumo Médio do Cliente: {consumo_medio:.2f}")
                else:
                    print("O resultado do consumo médio do cliente não está presente na resposta.")
            else:
                print("Erro ao obter o consumo médio do cliente.")

        elif opcao_relatorio == '4':
            limite_estoque = int(input("Digite o limite de estoque: "))
            resposta = f"{BASE_URL}/produtosBaixoEstoque"
            payload = {"limite": limite_estoque}

            try:
                response = requests.get(resposta, params=payload, headers={"Content-Type": "application/json"})

                if response.status_code == 200:
                    relatorio = response.json().get("produtos_baixo_estoque", [])
                    print("\nProdutos com Baixo Estoque:")
                    for produto, estoque in relatorio:
                        print(f"{produto} - Estoque: {estoque}")
                else:
                    print(f"Erro na requisição: {response.status_code}")
                    print(response.json())

            except Exception as e:
                print(f"Erro geral na requisição: {e}")


        elif opcao_relatorio == '5':
            pass

    elif opcao == '4':
        print("Saindo...")
        break