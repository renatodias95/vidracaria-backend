import sqlite3

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

# Listar todas as tabelas
print("Tabelas no banco:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
for row in cursor.fetchall():
    print("-", row[0])

# Listar colunas da tabela perfis
print("\nColunas da tabela perfis:")
cursor.execute("PRAGMA table_info(perfis);")
for col in cursor.fetchall():
    print("-", col)

conn.close()
