import sqlite3

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

tabelas = ["Orcamentos", "ItensOrcamento"]
for tabela in tabelas:
    print(f"Colunas da tabela {tabela}:")
    cursor.execute(f"PRAGMA table_info({tabela});")
    for col in cursor.fetchall():
        print("-", col)
    print()

conn.close()
