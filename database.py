import sqlite3
import hashlib

def create_db():
    conn = sqlite3.connect('estoque.db')
    c = conn.cursor()

    # Tabela de Categorias
    c.execute('''
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL
    )
    ''')

    # Tabela de Fornecedores
    c.execute('''
    CREATE TABLE IF NOT EXISTS fornecedores (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        contato TEXT
    )
    ''')

    # Tabela de Produtos
    c.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY,
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
        id INTEGER PRIMARY KEY,
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
        id INTEGER PRIMARY KEY,
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
        id INTEGER PRIMARY KEY,
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
    INSERT INTO funcionarios (nome, telefone, endereco, cargo, salario, senha, nivel, cpf)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', ('Admin', '123456789', 'Admin Address', 'Admin', '0', senha_hash, 'Admin', '000.000.000-00'))

    print("Tabelas criadas com sucesso.")
    conn.commit()
    conn.close()

def register_employee(nome, telefone, endereco, cargo, salario, senha, nivel, cpf):
    conn = sqlite3.connect('estoque.db')
    c = conn.cursor()
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    c.execute('''
    INSERT INTO funcionarios (nome, telefone, endereco, cargo, salario, senha, nivel, cpf)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nome, telefone, endereco, cargo, salario, senha_hash, nivel, cpf))
    conn.commit()
    conn.close()

def check_login(nome, senha):
    conn = sqlite3.connect('estoque.db')
    c = conn.cursor()
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    c.execute('SELECT * FROM funcionarios WHERE nome = ? AND senha = ?', (nome, senha_hash))
    result = c.fetchone()
    conn.close()
    return result

if __name__ == "__main__":
    create_db()

def create_clientes_table():
    conn = sqlite3.connect('C:/Users/ld388/Desktop/management/php/clientes.db')
    c = conn.cursor()
    
    # Cria a tabela clientes se não existir
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
    
    conn.commit()
    conn.close()

    # Tabela de Vendas
    c.execute('''
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY,
        produto_id INTEGER,
        quantidade INTEGER,
        total REAL,
        data_venda DATE DEFAULT (date('now')),
        forma_pagamento TEXT,
        status TEXT DEFAULT 'Preparação',
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
    ''')


if __name__ == "__main__":
    create_clientes_table()