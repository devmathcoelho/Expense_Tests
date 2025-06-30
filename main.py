import psycopg2
# Configurações do banco
try:
    conn = psycopg2.connect(
        dbname="database_name",
        user="user_name",
        password="password",
        host="localhost",
        port="5432",
        client_encoding='utf-8'
    )
    cursor = conn.cursor()
except Exception as e:
    print("Error to connect database:", e)
    sys.exit(1)


def show_menu():
    print("\n=== MONTHLY EXPENSES CALCULATOR ===")
    print("1. Add expense")
    print("2. View expense summary")
    print("3. Remove expense")
    print("4. Exit")

def add_expense():
    category = input("Enter the expense category: ").strip().lower()
    try:
        amount = float(input("Enter the expense amount: $ "))
    except ValueError:
        print("⚠️ Invalid amount.")
        return

    try:
        cursor.execute("INSERT INTO expenses (category, amount) VALUES (%s, %s)", (category, amount))
        conn.commit()
        print("✅ Expense added successfully!")
    except Exception as e:
        print("Error adding expense:", e)
        conn.rollback()

def view_summary():
    try:
        cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
        results = cursor.fetchall()

        if not results:
            print("📭 No expenses recorded.")
            return

        total = 0
        print("\n--- EXPENSE SUMMARY ---")
        for category, total_amount in results:
            print(f"{category.title()}: $ {total_amount:.2f}")
            total += total_amount
        print(f"\n💰 Total: $ {total:.2f}")
    except Exception as e:
        print("Error viewing summary:", e)

def remove_expense():
    view_expenses()
    try:
        expense_id = int(input("Enter the ID of the expense to remove: "))
        cursor.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
        conn.commit()
        print("🗑️ Expense removed successfully!")
    except ValueError:
        print("⚠️ Invalid ID.")
    except Exception as e:
        print("Error removing expense:", e)
        conn.rollback()

def view_expenses():
    try:
        cursor.execute("SELECT id, category, amount FROM expenses")
        records = cursor.fetchall()
        if not records:
            print("📭 No expenses recorded.")
            return
        print("\n--- EXPENSE LIST ---")
        for id, category, amount in records:
            print(f"ID: {id} | {category.title()} - $ {amount:.2f}")
    except Exception as e:
        print("Error listing expenses:", e)

def main():
    try:
        while True:
            show_menu()
            option = input("Choose an option: ")

            if option == '1':
                add_expense()
            elif option == '2':
                view_summary()
            elif option == '3':
                remove_expense()
            elif option == '4':
                print("👋 Exiting...")
                break
            else:
                print("❌ Invalid option.")
    except KeyboardInterrupt:
        print("\n👋 Program interrupted by user.")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
