#!/usr/bin/env python3
"""
Script para visualizar as tabelas do banco de dados alunos.db
"""
import sqlite3


def formatar_tabela(dados, headers):
    """Formata dados em uma tabela simples"""
    if not dados:
        return "   (Sem dados)"

    # Calcular largura de cada coluna
    col_widths = [len(str(h)) for h in headers]
    for row in dados:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))

    # Criar linha separadora
    separator = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"

    # Criar cabeçalho
    header_row = "|" + "|".join(f" {str(h):<{col_widths[i]}} " for i, h in enumerate(headers)) + "|"

    # Criar linhas de dados
    result = [separator, header_row, separator]
    for row in dados:
        data_row = "|" + "|".join(f" {str(val):<{col_widths[i]}} " for i, val in enumerate(row)) + "|"
        result.append(data_row)
    result.append(separator)

    return "\n".join(result)


def visualizar_database(db_path='alunos.db'):
    """Visualiza todas as tabelas e seus dados do banco de dados"""

    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Listar todas as tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tabelas = cursor.fetchall()

        if not tabelas:
            print("Nenhuma tabela encontrada no banco de dados.")
            return

        print(f"\n{'='*80}")
        print(f"BANCO DE DADOS: {db_path}")
        print(f"{'='*80}\n")
        print(f"Tabelas encontradas: {len(tabelas)}\n")

        # Para cada tabela, mostrar estrutura e dados
        for (tabela,) in tabelas:
            print(f"\n{'-'*80}")
            print(f"TABELA: {tabela}")
            print(f"{'-'*80}")

            # Obter informações das colunas
            cursor.execute(f"PRAGMA table_info({tabela});")
            colunas_info = cursor.fetchall()

            print("\nESTRUTURA:")
            estrutura = []
            for col in colunas_info:
                col_id, nome, tipo, not_null, default, pk = col
                estrutura.append([
                    nome,
                    tipo,
                    "SIM" if pk else "NAO",
                    "SIM" if not_null else "NAO",
                    default if default else "-"
                ])

            print(formatar_tabela(
                estrutura,
                ["Coluna", "Tipo", "Primary Key", "Not Null", "Default"]
            ))

            # Obter dados da tabela
            cursor.execute(f"SELECT * FROM {tabela};")
            dados = cursor.fetchall()

            print(f"\nDADOS ({len(dados)} registros):")

            if dados:
                # Nomes das colunas
                colunas = [desc[0] for desc in cursor.description]
                print(formatar_tabela(dados, colunas))
            else:
                print("   (Tabela vazia)")

        print(f"\n{'='*80}\n")

        # Fechar conexão
        conn.close()

    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


if __name__ == "__main__":
    import sys

    # Permite passar o caminho do banco como argumento
    db_path = sys.argv[1] if len(sys.argv) > 1 else 'alunos.db'

    print("\nVisualizador de Banco de Dados SQLite\n")
    visualizar_database(db_path)
