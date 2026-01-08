import json
import psycopg2
from psycopg2 import sql

DB_NAME = "AUTOSALON"
DB_USER = "postgres"
DB_PASSWORD = "1"
DB_HOST = "localhost"
DB_PORT = "5432"

JSON_FILE = "../data/cars.json"

def create_table(cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS cars (
        id SERIAL PRIMARY KEY,
        firm VARCHAR(100) NOT NULL,
        model VARCHAR(100) NOT NULL,
        year INTEGER NOT NULL,
        power INTEGER NOT NULL,
        color VARCHAR(50) NOT NULL,
        price DECIMAL(12, 2) NOT NULL
    );
    """
    cursor.execute(create_table_query)
    print("Таблица 'cars' создана.")

def insert_car(cursor, car):
    """Вставка одной машины в таблицу"""
    insert_query = """
    INSERT INTO cars (firm, model, year, power, color, price)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (
        car["firm"],
        car["model"],
        car["year"],
        car["power"],
        car["color"],
        car["price"]
    ))

def main():
    # Чтение JSON
    with open(JSON_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    cars_list = data.get("cars", [])
    print(f"Прочитано {len(cars_list)} автомобилей из JSON.")

    # Подключение к БД
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        # Создаём таблицу
        create_table(cursor)

        # Вставляем данные
        for car in cars_list:
            insert_car(cursor, car)

        # Сохраняем изменения
        conn.commit()
        print(f"Успешно добавлено {len(cars_list)} записей в таблицу 'cars'.")

    except Exception as e:
        print(f"Ошибка: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    main()