import psycopg2
from psycopg2 import sql

# Параметри підключення до бази даних
conn = psycopg2.connect(
    dbname="library",
    user="user",
    password="password",
    host="127.0.0.1",
    port="5432"
)

cursor = conn.cursor()

# Створення таблиць
cursor.execute("""
CREATE TABLE IF NOT EXISTS Books (
    inventory_number SERIAL PRIMARY KEY,
    author VARCHAR(255),
    title VARCHAR(255),
    section VARCHAR(50) CHECK (section IN ('технічна', 'художня', 'економічна')),
    publication_year INTEGER,
    page_count INTEGER,
    price NUMERIC(10, 2),
    type VARCHAR(50) CHECK (type IN ('посібник', 'книга', 'періодичне видання')),
    quantity INTEGER,
    max_days_with_reader INTEGER
);

CREATE TABLE IF NOT EXISTS Readers (
    ticket_number SERIAL PRIMARY KEY,
    last_name VARCHAR(100),
    first_name VARCHAR(100),
    phone CHAR(10),
    address VARCHAR(255),
    course INTEGER CHECK (course BETWEEN 1 AND 4),
    group_name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS BookIssues (
    issue_id SERIAL PRIMARY KEY,
    issue_date DATE,
    reader_ticket_number INTEGER REFERENCES Readers(ticket_number) ON DELETE CASCADE,
    book_inventory_number INTEGER REFERENCES Books(inventory_number) ON DELETE CASCADE
);
""")

# Заповнення таблиць даними
books_data = [
    ('Author1', 'Book Title 1', 'технічна', 2015, 320, 12.5, 'книга', 5, 14),
    # ... 13 інших книг
]

readers_data = [
    ('Smith', 'John', '1234567890', '123 Main St', 1, 'CS101'),
    # ... 8 інших читачів
]

issues_data = [
    ('2023-11-01', 1, 1),
    # ... 10 інших видач
]

# Додавання даних до таблиць
cursor.executemany("""
    INSERT INTO Books (author, title, section, publication_year, page_count, price, type, quantity, max_days_with_reader)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
""", books_data)

cursor.executemany("""
    INSERT INTO Readers (last_name, first_name, phone, address, course, group_name)
    VALUES (%s, %s, %s, %s, %s, %s);
""", readers_data)

cursor.executemany("""
    INSERT INTO BookIssues (issue_date, reader_ticket_number, book_inventory_number)
    VALUES (%s, %s, %s);
""", issues_data)

# Підтвердження змін та закриття з'єднання
conn.commit()
cursor.close()
conn.close()

print("Дані успішно створені!")