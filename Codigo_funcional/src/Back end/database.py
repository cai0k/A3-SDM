import logging
import sqlite3
from typing import List, Tuple
from datetime import datetime, date
import uuid


def conectar_banco():
    return sqlite3.connect('loja.db')


def criar_tabelas():
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            ClienteID INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            ProdutoID INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            estoque INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Vendas (
            VendaID INTEGER PRIMARY KEY,
            ClienteID INTEGER,
            ProdutoID INTEGER,
            QuantidadeVendida INTEGER,
            DataVenda DATE,
            FOREIGN KEY (ClienteID) REFERENCES clientes(ClienteID),
            FOREIGN KEY (ProdutoID) REFERENCES produtos(ProdutoID)
        )
    ''')

    conn.commit()
    conn.close()


def verificar_banco():
    connection = conectar_banco()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM clientes")
    numero_registros = cursor.fetchone()[0]

    connection.close()

    return numero_registros == 0


def preencher_tabelas():
    if verificar_banco():
        connection = conectar_banco()
        cursor = connection.cursor()

        for i in range(1, 11):
            cursor.execute(f"INSERT INTO clientes (nome, email) VALUES ('Cliente{i}', 'cliente{i}@email.com')")

        for i in range(1, 11):
            produto_codigo = str(uuid.uuid4().hex)[:8]
            cursor.execute(f"INSERT INTO Produtos (nome, preco, estoque, codigo) VALUES ('Produto{i}', {i * 10}, {50 - i}, '{produto_codigo}')")

        data_venda = date.today()
        for i in range(1, 11):
            cursor.execute(f"INSERT INTO Vendas (DataVenda, ClienteID, ProdutoID, QuantidadeVendida) VALUES ('{data_venda}', {i}, {i}, {i * 2})")

        connection.commit()
        connection.close()


def adicionar_cliente(nome, email):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO clientes (nome, email) VALUES (?, ?)', (nome, email))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao cadastrar cliente: {e}")
        conn.rollback()
        conn.close()
        return False


def selecionar_cliente(ClienteID):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clientes WHERE ClienteID = ?', (ClienteID,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado
    except Exception as e:
        print(f"Erro ao selecionar cliente: {e}")
        conn.rollback()
        conn.close()
        return False
    

def listar_clientes():
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clientes')
        clientes = cursor.fetchall()
        conn.close()
        return clientes

    except Exception as e:
        print(f"Erro ao listar clientes: {e}")
        return None


def update_cliente(nome, novo_nome, novo_email):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('UPDATE clientes SET nome = ?, email = ? WHERE nome = ?', (novo_nome, novo_email, nome))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao atualizar cliente: {e}")
        conn.rollback()
        conn.close()
        return False


def excluir_cliente(ClienteID):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM clientes WHERE ClienteID = ?', (ClienteID,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Erro ao exlcuir cliente: {e}")
        conn.rollback()
        conn.close()
        return False
    

def adicionar_produto(codigo, nome, preco, estoque):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO produtos (codigo, nome, preco, estoque) VALUES (?, ?, ?, ?)', (codigo, nome, preco, estoque))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Erro ao adicionar produto: {e}")
        conn.rollback()
        conn.close()
        return False


def listar_produtos():
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produtos')
        produtos = cursor.fetchall()
        conn.close()
        return produtos

    except Exception as e:
        print(f"Erro ao listar produtos: {e}")
        return None


def buscar_produto(codigo):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM produtos WHERE codigo = ?', (codigo,))
        produto = cursor.fetchone()

        conn.close()

        return produto

    except Exception as e:
        print(f"Erro ao buscar produto: {e}")
        return None


def atualizar_produto(codigo, novo_preco, novo_estoque):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute('UPDATE produtos SET preco = ?, estoque = ? WHERE codigo = ?', (novo_preco, novo_estoque, codigo))

        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Erro ao atualizar produto: {e}")


def excluir_produto(codigo):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM produtos WHERE codigo = ?', (codigo,))

        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Erro ao excluir produto: {e}")


def realizar_venda(ClienteID, ProdutoID, quantidade):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        logging.info(f"Tentando realizar venda para ClienteID: {ClienteID}, ProdutoID: {ProdutoID}, Quantidade: {quantidade}")

        cursor.execute('SELECT estoque FROM produtos WHERE ProdutoID = ?', (ProdutoID,))
        estoque_atual = cursor.fetchone()

        if estoque_atual is not None:
            estoque_atual = estoque_atual[0]
        else:
            logging.error("Produto não encontrado.")
            conn.close()
            return False

        logging.info(f"Estoque atual para ProdutoID {ProdutoID}: {estoque_atual}")

        if int(estoque_atual) < int(quantidade):
            logging.error("Estoque insuficiente para realizar a venda.")
            conn.close()
            return False

        novo_estoque = int(estoque_atual) - int(quantidade)

        cursor.execute('UPDATE produtos SET estoque = ? WHERE ProdutoID = ?', (novo_estoque, ProdutoID))

        data_venda = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('INSERT INTO Vendas (DataVenda, ClienteID, ProdutoID, QuantidadeVendida) VALUES (?, ?, ?, ?)',
                       (data_venda, ClienteID, ProdutoID, quantidade))

        conn.commit()
        conn.close()
        logging.info("Venda realizada com sucesso.")
        return True

    except Exception as e:
        logging.error(f"Erro durante a realização da venda: {e}")
        conn.rollback()  
        conn.close()
        return False



def produtos_mais_vendidos(cursor) -> List[Tuple[str, int]]:
    try:
        cursor.execute('''
            SELECT p.nome, SUM(v.QuantidadeVendida) as total_vendido
            FROM produtos p
            JOIN Vendas v ON p.ProdutoID = v.ProdutoID
            GROUP BY p.ProdutoID
            ORDER BY total_vendido DESC
            LIMIT 5
        ''')
        return cursor.fetchall()

    except Exception as e:
        print(f"Erro ao obter produtos mais vendidos: {e}")
        return []


def produtos_por_cliente(cursor, cliente_id: int) -> List[Tuple[str, int]]:
    try:
        cursor.execute('''
            SELECT p.nome, SUM(v.QuantidadeVendida) as total_comprado
            FROM produtos p
            JOIN Vendas v ON p.ProdutoID = v.ProdutoID
            WHERE v.ClienteID = ?
            GROUP BY p.ProdutoID
            ORDER BY total_comprado DESC
        ''', (cliente_id,))
        return cursor.fetchall()

    except Exception as e:
        print(f"Erro ao obter produtos por cliente: {e}")
        return []


def consumo_medio_cliente(cursor, cliente_id: int) -> float:
    try:
        cursor.execute('''
            SELECT AVG(v.QuantidadeVendida) as consumo_medio
            FROM Vendas v
            WHERE v.ClienteID = ?
        ''', (cliente_id,))
        return cursor.fetchone()[0] or 0.0

    except Exception as e:
        print(f"Erro ao obter consumo médio do cliente: {e}")
        return 0.0


def produtos_baixo_estoque(cursor, limite: int) -> List[Tuple[str, int]]:
    try:
        cursor.execute('''
            SELECT nome, estoque
            FROM produtos
            WHERE estoque < ?
        ''', (limite,))
        return cursor.fetchall()

    except Exception as e:
        print(f"Erro ao obter produtos com baixo estoque: {e}")
        raise