import sqlite3

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

# Listar colunas da tabela PerfisAluminio
print("Colunas da tabela PerfisAluminio:")
cursor.execute("PRAGMA table_info(PerfisAluminio);")
for col in cursor.fetchall():
    print("-", col)

# Listar os 5 primeiros perfis
print("\nPrimeiros registros de PerfisAluminio:")
cursor.execute("SELECT * FROM PerfisAluminio LIMIT 5;")
for row in cursor.fetchall():
    print("-", row)

conn.close()
