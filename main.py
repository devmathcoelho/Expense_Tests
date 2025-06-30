import psycopg2
# Configurações do banco
try:
    conn = psycopg2.connect(
        dbname="expense_test",
        user="postgres",
        password="Aranha4667@",
        host="localhost",
        port="5432",
        client_encoding='utf-8'
    )
    cursor = conn.cursor()
except Exception as e:
    print("Erro ao conectar no banco:", e)
    sys.exit(1)


def mostrar_menu():
    print("\n=== CALCULADORA DE GASTOS MENSAIS ===")
    print("1. Adicionar gasto")
    print("2. Ver resumo de gastos")
    print("3. Remover gasto")
    print("4. Sair")

def adicionar_gasto():
    categoria = input("Digite a categoria do gasto: ").strip().lower()
    try:
        valor = float(input("Digite o valor do gasto: R$ "))
    except ValueError:
        print("⚠️ Valor inválido.")
        return

    try:
        cursor.execute("INSERT INTO gastos (categoria, valor) VALUES (%s, %s)", (categoria, valor))
        conn.commit()
        print("✅ Gasto adicionado com sucesso!")
    except Exception as e:
        print("Erro ao adicionar gasto:", e)
        conn.rollback()

def ver_resumo():
    try:
        cursor.execute("SELECT categoria, SUM(valor) FROM gastos GROUP BY categoria")
        resultados = cursor.fetchall()

        if not resultados:
            print("📭 Nenhum gasto registrado.")
            return

        total = 0
        print("\n--- RESUMO DE GASTOS ---")
        for categoria, soma in resultados:
            print(f"{categoria.title()}: R$ {soma:.2f}")
            total += soma
        print(f"\n💰 Total geral: R$ {total:.2f}")
    except Exception as e:
        print("Erro ao ver resumo:", e)

def remover_gasto():
    ver_gastos()
    try:
        id_gasto = int(input("Digite o ID do gasto que deseja remover: "))
        cursor.execute("DELETE FROM gastos WHERE id = %s", (id_gasto,))
        conn.commit()
        print("🗑️ Gasto removido com sucesso!")
    except ValueError:
        print("⚠️ ID inválido.")
    except Exception as e:
        print("Erro ao remover gasto:", e)
        conn.rollback()

def ver_gastos():
    try:
        cursor.execute("SELECT id, categoria, valor FROM gastos")
        registros = cursor.fetchall()
        if not registros:
            print("📭 Nenhum gasto registrado.")
            return
        print("\n--- LISTA DE GASTOS ---")
        for id, categoria, valor in registros:
            print(f"ID: {id} | {categoria.title()} - R$ {valor:.2f}")
    except Exception as e:
        print("Erro ao listar gastos:", e)

def main():
    try:
        while True:
            mostrar_menu()
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                adicionar_gasto()
            elif opcao == '2':
                ver_resumo()
            elif opcao == '3':
                remover_gasto()
            elif opcao == '4':
                print("👋 Saindo...")
                break
            else:
                print("❌ Opção inválida.")
    except KeyboardInterrupt:
        print("\n👋 Programa interrompido pelo usuário.")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()