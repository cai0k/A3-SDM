from flask import Flask, jsonify, request
from cliente import GerenciadorClientes
from estoque import GerenciadorEstoque
from database import conectar_banco, criar_tabelas, adicionar_cliente, selecionar_cliente, update_cliente, excluir_cliente, adicionar_produto, listar_produtos, buscar_produto, atualizar_produto, excluir_produto, realizar_venda, preencher_tabelas, produtos_mais_vendidos, produtos_por_cliente, consumo_medio_cliente, produtos_baixo_estoque, listar_clientes
from database import conectar_banco, preencher_tabelas



connection = conectar_banco()
conectar_banco()
criar_tabelas()
preencher_tabelas()
gerenciador_clientes = GerenciadorClientes()
gerenciador_estoque = GerenciadorEstoque()


class StockInsufficientError(Exception):
    pass


def get_cursor():
    conn = conectar_banco()
    cursor = conn.cursor()
    return conn, cursor


def close_connection(conn):
    conn.close()


app = Flask(__name__)


@app.route('/cadastrarCliente', methods=['POST'])
def adicionar_cliente_api():
    dados = request.json
    nome = dados.get('nome')
    email = dados.get('email')
    adicionar_cliente(nome, email)
    return jsonify({"mensagem": "Cliente adicionado com sucesso!"})


@app.route('/buscarCliente/<int:id>', methods=['GET'])
def buscar_cliente_api(id):
    cliente = selecionar_cliente(id)
    
    if cliente:
        return jsonify({"cliente": cliente})
    else:
        return jsonify({"error": "Cliente não encontrado"})
    

@app.route('/listarClientes', methods=['GET'])
def listar_clientes_api():
    try:
        cliente = listar_clientes()
        if cliente is not None:
            clientes_json = [{"nome": clientes[1], "email": clientes[2]} for clientes in cliente]

            return jsonify({"clientes": clientes_json})
        else:
            return jsonify({"error": "Erro ao obter a lista de produtos"})

    except Exception as e:
        print(f"Erro geral na rota /listarClientes: {e}")
        return jsonify({"error": "Erro ao listar clientes"})
    

@app.route('/editarCliente', methods=['POST'])
def atualizar_cliente_api():
    dados = request.json
    nome = dados.get('nome')
    novo_nome = dados.get('novo_nome')
    novo_email = dados.get('novo_email')
    cliente = update_cliente(nome, novo_nome, novo_email)
    if cliente:
        return jsonify({"cliente": cliente})
    else:
        return jsonify({"error": "Falha ao atualizar cliente"})
    

@app.route('/excluirCliente', methods=['DELETE'])
def excluir_cliente_api():
    dados = request.json
    id = dados.get('id')
    cliente = excluir_cliente(id)
    if cliente:
        return jsonify({"mensagem": "Cliente excluído com sucesso"})
    else:
        return jsonify({"error": "Falha ao excluir cliente"})
    

@app.route('/adicionarProduto', methods=['POST'])
def adicionar_produto_api():
    dados = request.json
    codigo = dados.get('codigo')
    nome = dados.get('nome')
    preco = dados.get('preco')
    estoque = dados.get('estoque')
    sucesso = adicionar_produto(codigo, nome, preco, estoque)
    if sucesso:
        return jsonify({"mensagem": "Produto adicionado com sucesso"})
    else:
        return jsonify({"error": "Falha ao adicionar produto"})
    

@app.route('/listarProdutos', methods=['GET'])
def listar_produtos_api():
    try:
        produtos = listar_produtos()
        if produtos is not None:
            produtos_json = [{"codigo": produto[1], "nome": produto[2], "preco": produto[3], "estoque": produto[4]} for produto in produtos]

            return jsonify({"produtos": produtos_json})
        else:
            return jsonify({"error": "Erro ao obter a lista de produtos"})

    except Exception as e:
        print(f"Erro geral na rota /listarProdutos: {e}")
        return jsonify({"error": "Erro ao listar produtos"})
    

@app.route('/buscarProduto', methods=['GET'])
def buscar_produto_api():
    dados = request.json
    codigo = dados.get('codigo')
    produto = buscar_produto(codigo)
    if produto:
        return jsonify({"produto": produto})
    else:
        return jsonify({"error": "Produto não encontrado"}), 404


@app.route('/atualizarProduto', methods=['POST'])
def atualizar_produto_api():
    try:
        dados = request.json
        codigo = dados.get('codigo')
        novo_preco = dados.get('novo_preco')
        novo_estoque = dados.get('novo_estoque')
        atualizar_produto(codigo, novo_preco, novo_estoque)
        return jsonify({"mensagem": "Produto atualizado com sucesso"})
    except Exception as e:
        return jsonify({"error": f"Erro ao atualizar produto: {e}"})


@app.route('/excluirProduto', methods=['DELETE'])
def excluir_produto_api():
    dados = request.json
    codigo = dados.get('codigo')
    excluir_produto(codigo)
    return jsonify({"mensagem": "Produto excluído com sucesso"})


@app.route('/realizarVenda', methods=['POST'])
def realizar_venda_api():
    dados = request.json
    ClienteID = dados.get('ClienteID')
    ProdutoID = dados.get('ProdutoID')
    QuantidadeVendida = dados.get('QuantidadeVendida')
    sucesso = realizar_venda(ClienteID, ProdutoID, QuantidadeVendida)
    if sucesso:
        return jsonify({"Venda realizada com sucesso": sucesso})
    else:
        return jsonify({"error": "Estoque insuficiente para realizar a venda"})



@app.route('/produtosMaisVendidos', methods=['GET'])
def produtos_mais_vendidos_api():
    conn, cursor = get_cursor()
    resultados = produtos_mais_vendidos(cursor)
    close_connection(conn)
    return jsonify({"produtos_mais_vendidos": resultados})


@app.route('/produtos_por_cliente/<int:cliente_id>', methods=['GET'])
def rota_produtos_por_cliente(cliente_id):
    try:
        conn, cursor = get_cursor()

        resultados = produtos_por_cliente(cursor, cliente_id)

        close_connection(conn)

        return jsonify(resultados)

    except Exception as e:
        return jsonify({'erro': f'Erro ao obter produtos por cliente: {str(e)}'})


@app.route('/consumoMedioCliente/<int:cliente_id>', methods=['GET'])
def consumo_medio_cliente_api(cliente_id):

    if cliente_id is None:
        return jsonify({"error": "O parâmetro 'id' é obrigatório"})
    try:
        conn, cursor = get_cursor()
        resultado = consumo_medio_cliente(cursor, cliente_id)
        close_connection(conn)
        return jsonify({"consumo_medio_cliente": resultado})
    except Exception as e:
        print(f"Erro geral na rota /consumoMedioCliente: {e}")
        return jsonify({"error": "Erro ao obter consumo médio do cliente"})


@app.route('/produtosBaixoEstoque', methods=['GET'])
def produtos_baixo_estoque_api():
    limite = request.args.get('limite')

    if limite is None:
        return jsonify({"error": "O parâmetro 'limite' é obrigatório"})

    try:
        conn, cursor = get_cursor()
        resultados = produtos_baixo_estoque(cursor, int(limite))
        close_connection(conn)
        return jsonify({"produtos_baixo_estoque": resultados})

    except Exception as e:
        print(f"Erro geral na rota /produtosBaixoEstoque: {e}")
        return jsonify({"error": "Erro ao obter produtos com baixo estoque"})

    

connection.close()

    
if __name__ == '__main__':
    app.run(debug=True)