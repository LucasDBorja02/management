import sqlite3
import os

def create_carrinho_db():
    # Diretório onde o banco de dados será criado
    db_path = 'C:/Users/ld388/Desktop/management/site/pages/database_carrinho.db'

    # Conectar ou criar o banco de dados
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Criar a tabela "carrinho" se não existir
    c.execute('''
    CREATE TABLE IF NOT EXISTS carrinho (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER NOT NULL,
        nome TEXT NOT NULL,
        preco REAL NOT NULL,
        quantidade INTEGER NOT NULL,
        data_adicionado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Fechar a conexão
    conn.commit()
    conn.close()
    print(f"Banco de dados criado com sucesso em: {db_path}")

if __name__ == "__main__":
    create_carrinho_db()
