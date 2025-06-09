import sqlite3

# Caminho relativo do banco, ajuste se necessário
conn = sqlite3.connect('../db.sqlite3')
cursor = conn.cursor()

# Listar todas as tabelas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = cursor.fetchall()

print("Tabelas encontradas no banco:")
for tabela in tabelas:
    print(tabela[0])

conn.close()
