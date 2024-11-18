import psycopg2
from psycopg2 import sql
from datetime import timedelta

def format_output(cursor):
    """Виводить результати запиту у форматованому вигляді."""
    headers = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    # Визначення ширини кожного стовпця
    col_widths = [max(len(str(row[i])) for row in rows + [headers]) for i in range(len(headers))]

    # Форматування заголовків
    header_row = " | ".join(f"{header:<{col_widths[i]}}" for i, header in enumerate(headers))
    separator = "-+-".join("-" * col_widths[i] for i in range(len(headers)))

    # Форматування рядків даних
    data_rows = "\n".join(
        " | ".join(f"{str(row[i]):<{col_widths[i]}}" for i in range(len(row))) for row in rows
    )

    print(header_row)
    print(separator)
    print(data_rows)


def execute_queries(cursor):
    """Виконання запитів згідно із завданням."""
    print("1. Всі книги, які були видані після 2001 року. Назви за алфавітом:")
    cursor.execute("""
        SELECT title, author, publication_year
        FROM Books
        WHERE publication_year > 2001
        ORDER BY title ASC;
    """)
    format_output(cursor)
    print()

    print("2. Кількість книг кожного виду:")
    cursor.execute("""
        SELECT type, COUNT(*) AS count
        FROM Books
        GROUP BY type;
    """)
    format_output(cursor)
    print()

    print("3. Всі читачі, які брали посібники. Прізвища за алфавітом:")
    cursor.execute("""
        SELECT DISTINCT r.last_name, r.first_name
        FROM BookIssues bi
        JOIN Readers r ON bi.reader_ticket_number = r.ticket_number
        JOIN Books b ON bi.book_inventory_number = b.inventory_number
        WHERE b.type = 'посібник'
        ORDER BY r.last_name ASC;
    """)
    format_output(cursor)
    print()

    print("4. Всі книги за указаним розділом (наприклад, 'технічна'):")
    section_param = 'технічна'  # Змінюйте значення для інших розділів
    cursor.execute("""
        SELECT title, author, section
        FROM Books
        WHERE section = %s;
    """, (section_param,))
    format_output(cursor)
    print()

    print("5. Кінцевий термін повернення кожної книги, яка була видана читачу:")
    cursor.execute("""
        SELECT b.title, r.last_name, r.first_name, bi.issue_date,
               bi.issue_date + b.max_days_with_reader * INTERVAL '1 day' AS return_date
        FROM BookIssues bi
        JOIN Books b ON bi.book_inventory_number = b.inventory_number
        JOIN Readers r ON bi.reader_ticket_number = r.ticket_number;
    """)
    format_output(cursor)
    print()

    print("6. Кількість посібників, книг та періодичних видань у кожному розділі:")
    cursor.execute("""
        SELECT section, type, COUNT(*) AS count
        FROM Books
        GROUP BY section, type
        ORDER BY section, type;
    """)
    format_output(cursor)
    print()


def main():
    # Параметри підключення до бази даних
    conn = psycopg2.connect(
        dbname="library",
        user="user",
        password="password",
        host="127.0.0.1",
        port="5432"
    )
    
    cursor = conn.cursor()

    # Виконання запитів
    execute_queries(cursor)

    # Закриття з'єднання
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
