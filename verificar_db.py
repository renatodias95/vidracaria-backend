import sqlite3

def verificar_estrutura_db():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    
    # Verificar tabelas existentes
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print("Tabelas existentes:", cursor.fetchall())
    
    # Verificar colunas da tabela PerfisAluminio
    try:
        cursor.execute("PRAGMA table_info(PerfisAluminio)")
        colunas = cursor.fetchall()
        print("\nColunas de PerfisAluminio:")
        for col in colunas:
            print(f"- {col[1]} ({col[2]})")
    except sqlite3.OperationalError as e:
        print(f"\nErro ao verificar PerfisAluminio: {e}")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    verificar_estrutura_db()
