import json
import psycopg2
import random
from psycopg2 import sql

# Параметры подключения к БД
DB_NAME = "AUTOSALON"
DB_USER = "postgres"
DB_PASSWORD = "1"
DB_HOST = "localhost"
DB_PORT = "5432"

#может сломаться, тогда полный путь прописать
DEALERS_FILE = "../data/dilers.json"
CARS_FILE = "../data/cars.json"


def create_dealers_table(cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS dealers (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        city VARCHAR(100) NOT NULL,
        address VARCHAR(200) NOT NULL,
        area VARCHAR(100),
        rating DECIMAL(3, 1) NOT NULL
    );
    """
    cursor.execute(create_table_query)
    print("Таблица 'dealers' создана.")


def add_dealer_id_to_cars(cursor):
    try:
        # Проверяем, существует ли столбец dealer_id
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='cars' AND column_name='dealer_id';
        """)

        if not cursor.fetchone():
            # Добавляем столбец dealer_id
            cursor.execute("""
                ALTER TABLE cars 
                ADD COLUMN dealer_id INTEGER;
            """)

            # Добавляем внешний ключ
            cursor.execute("""
                ALTER TABLE cars 
                ADD CONSTRAINT fk_dealer 
                FOREIGN KEY (dealer_id) 
                REFERENCES dealers(id) 
                ON DELETE SET NULL;
            """)
            print("Столбец 'dealer_id' добавлен в таблицу 'cars'.")
        else:
            print("Столбец 'dealer_id' уже существует в таблице 'cars'.")

    except Exception as e:
        print(f"Ошибка при добавлении столбца dealer_id: {e}")


def insert_dealer(cursor, dealer):
    """Вставка одного дилера в таблицу"""
    insert_query = """
    INSERT INTO dealers (name, city, address, area, rating)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id;
    """
    cursor.execute(insert_query, (
        dealer["Name"],
        dealer["City"],
        dealer["Address"],
        dealer["Area"],
        dealer["Rating"]
    ))
    return cursor.fetchone()[0]


def link_cars_to_dealers(cursor, dealer_ids):
    """Связывание автомобилей с дилерами в случайном порядке"""
    # Получаем все id автомобилей
    cursor.execute("SELECT id FROM cars WHERE dealer_id IS NULL;")
    car_ids = [row[0] for row in cursor.fetchall()]

    if not car_ids:
        print("Все автомобили уже имеют дилеров.")
        return

    print(f"Найдено {len(car_ids)} автомобилей без дилеров.")

    # Случайным образом назначаем дилеров автомобилям
    # Один дилер может иметь несколько автомобилей
    for car_id in car_ids:
        dealer_id = random.choice(dealer_ids)
        cursor.execute(
            "UPDATE cars SET dealer_id = %s WHERE id = %s",
            (dealer_id, car_id)
        )

    print(f"Автомобили успешно связаны с дилерами.")


def clear_dealers_data(cursor):
    """Очистка данных о дилерах (для перезапуска)"""
    try:
        # Сначала удаляем связи с автомобилями
        cursor.execute("UPDATE cars SET dealer_id = NULL;")

        # Затем очищаем таблицу дилеров
        cursor.execute("DELETE FROM dealers;")

        # Сбрасываем последовательность id
        cursor.execute("ALTER SEQUENCE dealers_id_seq RESTART WITH 1;")

        print("Данные дилеров очищены.")
    except Exception as e:
        print(f"Ошибка при очистке данных: {e}")


def main():
    # Чтение дилеров из JSON
    with open(DEALERS_FILE, "r", encoding="utf-8") as file:
        dealers_list = json.load(file)

    print(f"Прочитано {len(dealers_list)} дилеров из JSON.")

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

        # Очищаем старые данные
        clear_dealers_data(cursor)
        conn.commit()

        # Создаём таблицу дилеров
        create_dealers_table(cursor)

        # Добавляем столбец dealer_id в таблицу cars
        add_dealer_id_to_cars(cursor)

        # Вставляем дилеров и собираем их id
        dealer_ids = []
        for dealer in dealers_list:
            dealer_id = insert_dealer(cursor, dealer)
            dealer_ids.append(dealer_id)

        print(f"Успешно добавлено {len(dealer_ids)} дилеров в таблицу 'dealers'.")

        # Связываем автомобили с дилерами в случайном порядке
        link_cars_to_dealers(cursor, dealer_ids)

        # Сохраняем изменения
        conn.commit()
        print("Все операции успешно завершены.")

        # Выводим статистику
        cursor.execute("""
            SELECT d.name, COUNT(c.id) as car_count
            FROM dealers d
            LEFT JOIN cars c ON d.id = c.dealer_id
            GROUP BY d.id, d.name
            ORDER BY car_count DESC;
        """)

        print("\nСтатистика по дилерам:")
        print("-" * 40)
        for row in cursor.fetchall():
            print(f"{row[0]}: {row[1]} автомобилей")

        cursor.execute("SELECT COUNT(*) FROM cars WHERE dealer_id IS NOT NULL;")
        linked_cars = cursor.fetchone()[0]
        print(f"\nВсего связано автомобилей: {linked_cars}")

    except Exception as e:
        print(f"Ошибка: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def test_connection():
    """Тест подключения к БД"""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Подключение к БД успешно!")
        conn.close()
        return True
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return False


if __name__ == "__main__":
    # Сначала тестируем подключение
    if test_connection():
        main()