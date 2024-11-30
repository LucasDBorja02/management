import sqlite3
import hashlib

# Função para criar o banco de dados do estoque
def create_estoque_db():
    conn = sqlite3.connect('estoque.db')
    c = conn.cursor()

    # Tabela de Categorias
    c.execute('''
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    ''')

    # Tabela de Fornecedores
    c.execute('''
    CREATE TABLE IF NOT EXISTS fornecedores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        contato TEXT
    )
    ''')

    # Tabela de Produtos
    c.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco_compra REAL NOT NULL,
        preco_venda REAL NOT NULL,
        quantidade INTEGER NOT NULL,
        fornecedor TEXT,
        estoque_minimo INTEGER NOT NULL DEFAULT 0
    )
    ''')

    # Tabela de Vendas
    c.execute('''
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER,
        quantidade INTEGER,
        total REAL,
        data_venda DATE DEFAULT (date('now')),
        forma_pagamento TEXT,
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
    ''')

    # Tabela de Ajustes de Estoque
    c.execute('''
    CREATE TABLE IF NOT EXISTS ajustes_estoque (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER,
        quantidade_ajustada INTEGER,
        motivo TEXT,
        data_ajuste DATE DEFAULT (date('now')),
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
    ''')

    # Tabela de Contas
    c.execute('''
    CREATE TABLE IF NOT EXISTS contas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        valor REAL NOT NULL,
        data_conta DATE DEFAULT (date('now'))
    )
    ''')

    # Tabela de Funcionários
    c.execute('''
    CREATE TABLE IF NOT EXISTS funcionarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT NOT NULL,
        endereco TEXT NOT NULL,
        cargo TEXT NOT NULL,
        salario TEXT NOT NULL,
        senha TEXT NOT NULL,
        nivel TEXT NOT NULL,
        cpf TEXT
    )
    ''')

    # Inserir usuário Admin padrão
    senha_hash = hashlib.sha256('Admin'.encode()).hexdigest()
    c.execute('''
    INSERT OR IGNORE INTO funcionarios (nome, telefone, endereco, cargo, salario, senha, nivel, cpf)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', ('Admin', '123456789', 'Admin Address', 'Admin', '0', senha_hash, 'Admin', '000.000.000-00'))

    print("Banco de dados 'estoque.db' criado com sucesso.")
    conn.commit()
    conn.close()


# Função para criar o banco de dados de clientes
def create_clientes_db():
    conn = sqlite3.connect('clientes.db')
    c = conn.cursor()

    # Tabela de Clientes
    c.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT NOT NULL UNIQUE,
        endereco TEXT NOT NULL,
        telefone TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    )
    ''')

    print("Banco de dados 'clientes.db' criado com sucesso.")
    conn.commit()
    conn.close()


# Função principal que cria ambos os bancos de dados
def create_databases():
    create_estoque_db()
    create_clientes_db()
    print("Todos os bancos de dados foram criados com sucesso.")


if __name__ == "__main__":
    create_databases()
