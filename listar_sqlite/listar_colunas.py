import sqlite3

def listar_colunas(tabela):
    conn = sqlite3.connect('../db.sqlite3')
    cursor = conn.cursor()
    cursor.execute(f'PRAGMA table_info({tabela});')
    colunas = cursor.fetchall()
    print(f'Colunas da tabela {tabela}:')
    for coluna in colunas:
        print(f'- {coluna[1]} ({coluna[2]})')
    print()
    conn.close()

if __name__ == "__main__":
    listar_colunas('Acessorios')
    listar_colunas('Vidros')
