import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('vendas.db')

# Criar um cursor para executar as consultas
c = conn.cursor()

# Consultar todas as informações da tabela 'vendas'
c.execute("SELECT * FROM vendas")

# Buscar todos os resultados da consulta
vendas = c.fetchall()

# Exibir as informações da tabela
for venda in vendas:
    print(venda)

# Fechar a conexão com o banco de dados
conn.close()
