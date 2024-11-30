import sqlite3

def adicionar_coluna_status():
    conn = sqlite3.connect('C:/Users/ld388/Desktop/management/estoque.db')
    c = conn.cursor()

    # Tentar adicionar a coluna 'status', se ela não existir
    try:
        c.execute("ALTER TABLE vendas ADD COLUMN status TEXT DEFAULT 'Preparo'")
        conn.commit()
    except sqlite3.OperationalError as e:
        # Verificar se o erro é causado pela existência da coluna
        if "duplicate column name" in str(e).lower():
            print("A coluna 'status' já existe.")
        else:
            print(f"Erro ao tentar adicionar a coluna 'status': {e}")
    finally:
        conn.close()

def recriar_tabela_vendas():
    conn = sqlite3.connect('C:/Users/ld388/Desktop/management/estoque.db')
    c = conn.cursor()

    # Apagar a tabela 'vendas' se ela já existir
    c.execute("DROP TABLE IF EXISTS vendas")

    # Criar a tabela 'vendas' com a coluna 'status'
    c.execute('''
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        total REAL NOT NULL,
        forma_pagamento TEXT NOT NULL,
        data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'Preparo',
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
    ''')

    conn.commit()
    conn.close()

def criar_ou_atualizar_tabela_vendas():
    # Tentar adicionar a coluna 'status' primeiro
    adicionar_coluna_status()

    # Verificar se a tabela precisa ser recriada
    resposta = input("Você deseja recriar a tabela 'vendas'? Todos os dados serão perdidos. (s/n): ")
    if resposta.lower() == 's':
        recriar_tabela_vendas()
        print("Tabela 'vendas' recriada com sucesso.")
    else:
        print("A tabela 'vendas' não foi recriada.")

# Chame a função principal para criar ou atualizar a tabela
criar_ou_atualizar_tabela_vendas()
