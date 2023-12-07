import sqlite3
from sqlite3 import Cursor
from typing import List, Tuple
from datetime import datetime, date


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
            codigo INTEGER,
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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS EstoqueMinimo (
            EstoqueID INTEGER PRIMARY KEY,
            QuantidadeMinima INTEGER,
            ProdutoID INTEGER,
            FOREIGN KEY (ProdutoID) REFERENCES produtos(ProdutoID)
        )
    ''')

    conn.commit()
    conn.close()


def preencher_tabelas():
    connection = conectar_banco()
    cursor = connection.cursor()

    for i in range(1, 11):
        cursor.execute(f"INSERT INTO clientes (nome, email) VALUES ('Cliente{i}', 'cliente{i}@email.com')")

    for i in range(1, 11):
        cursor.execute(f"INSERT INTO Produtos (nome, preco, estoque) VALUES ('Produto{i}', {i * 10}, {50 - i})")

    data_venda = date.today()
    for i in range(1, 11):
        cursor.execute(f"INSERT INTO Vendas (DataVenda, ClienteID, ProdutoID, QuantidadeVendida) VALUES ('{data_venda}', {i}, {i}, {i * 2})")

    connection.commit()
    connection.close()


def adicionar_cliente(nome, email):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute('INSERT INTO clientes (nome, email) VALUES (?, ?)', (nome, email))

    conn.commit()
    conn.close()


def selecionar_cliente(ClienteID):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM clientes WHERE ClienteID = ?', (ClienteID,))
    resultado = cursor.fetchone()

    conn.close()

    return resultado


def update_cliente(nome, novo_nome, novo_email):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute('UPDATE clientes SET nome = ?, email = ? WHERE nome = ?', (novo_nome, novo_email, nome))

    conn.commit()
    conn.close()


def excluir_cliente(ClienteID):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM clientes WHERE ClienteID = ?', (ClienteID,))

    conn.commit()
    conn.close()


def adicionar_produto(codigo, nome, preco, estoque):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute('INSERT INTO produtos (codigo, nome, preco, estoque) VALUES (?, ?, ?, ?)', (codigo, nome, preco, estoque))

    conn.commit()
    conn.close()


def listar_produtos():
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()

    conn.close()

    return produtos


def buscar_produto(codigo):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM produtos WHERE codigo = ?', (codigo,))
    produto = cursor.fetchone()

    conn.close()

    return produto


def atualizar_produto(codigo, novo_preco, novo_estoque):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute('UPDATE produtos SET preco = ?, estoque = ? WHERE codigo = ?', (novo_preco, novo_estoque, codigo))

    conn.commit()
    conn.close()


def excluir_produto(codigo):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM produtos WHERE codigo = ?', (codigo,))

    conn.commit()
    conn.close()


def realizar_venda(ClienteID, ProdutoID, quantidade):
    conn = conectar_banco()
    cursor = conn.cursor()

    # Verifica se há estoque suficiente
    cursor.execute('SELECT estoque FROM produtos WHERE codigo = ?', (ProdutoID,))
    estoque_atual = cursor.fetchone()[0]

    if estoque_atual < quantidade:
        print("Estoque insuficiente para realizar a venda.")
        conn.close()
        return False

    novo_estoque = estoque_atual - quantidade

    cursor.execute('UPDATE produtos SET estoque = ? WHERE codigo = ?', (novo_estoque, ProdutoID))

    data_venda = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('INSERT INTO vendas (data_venda, ClienteID, ProdutoID, quantidade_vendida) VALUES (?, ?, ?, ?)',
                   (data_venda, ClienteID, ProdutoID, quantidade))

    conn.commit()
    conn.close()
    return True


def produtos_mais_vendidos(cursor) -> List[Tuple[str, int]]:
    cursor.execute('''
        SELECT p.nome, SUM(v.QuantidadeVendida) as total_vendido
        FROM produtos p
        JOIN Vendas v ON p.ProdutoID = v.ProdutoID
        GROUP BY p.ProdutoID
        ORDER BY total_vendido DESC
        LIMIT 5
    ''')
    return cursor.fetchall()


def produtos_por_cliente(cursor, cliente_id: int) -> List[Tuple[str, int]]:
    cursor.execute('''
        SELECT p.nome, SUM(v.QuantidadeVendida) as total_comprado
        FROM produtos p
        JOIN Vendas v ON p.ProdutoID = v.ProdutoID
        WHERE v.ClienteID = ?
        GROUP BY p.ProdutoID
        ORDER BY total_comprado DESC
    ''', (cliente_id,))
    return cursor.fetchall()


def consumo_medio_cliente(cursor, cliente_id: int) -> float:
    cursor.execute('''
        SELECT AVG(v.QuantidadeVendida) as consumo_medio
        FROM Vendas v
        WHERE v.ClienteID = ?
    ''', (cliente_id,))
    return cursor.fetchone()[0] or 0.0


def produtos_baixo_estoque(cursor, limite: int) -> List[Tuple[str, int]]:
    cursor.execute('''
        SELECT nome, estoque
        FROM produtos
        WHERE estoque < ?
    ''', (limite,))
    return cursor.fetchall()