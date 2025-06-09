import sqlite3

def listar_perfis():
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        
        # Verificar se a tabela existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='PerfisAluminio';")
        if not cursor.fetchone():
            print("A tabela PerfisAluminio não existe!")
            return
            
        # Listar colunas
        print("\nColunas da tabela PerfisAluminio:")
        cursor.execute("PRAGMA table_info(PerfisAluminio);")
        for col in cursor.fetchall():
            print(f"- {col[1]} ({col[2]})")
        
        # Contar registros
        cursor.execute("SELECT COUNT(*) FROM PerfisAluminio;")
        count = cursor.fetchone()[0]
        print(f"\nTotal de perfis cadastrados: {count}")
        
        # Listar os primeiros 5 perfis
        if count > 0:
            print("\nPrimeiros 5 perfis:")
            cursor.execute("SELECT * FROM PerfisAluminio LIMIT 5;")
            for row in cursor.fetchall():
                print(f"- {row}")
        
    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("Verificando perfis no banco de dados...")
    listar_perfis()
