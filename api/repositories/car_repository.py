from api.db import get_db_connection


class CarRepository:

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cars ORDER BY id')
        rows = cursor.fetchall()

        cars = []
        for row in rows:
            cars.append({
                'id': row[0],
                'firm': row[1],
                'model': row[2],
                'year': row[3],
                'power': row[4],
                'color': row[5],
                'price': float(row[6]),
                'dealer_id': row[7]
            })

        cursor.close()
        conn.close()
        return cars

    @staticmethod
    def get_by_id(car_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cars WHERE id = %s', (car_id,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return {
                'id': row[0],
                'firm': row[1],
                'model': row[2],
                'year': row[3],
                'power': row[4],
                'color': row[5],
                'price': float(row[6]),
                'dealer_id': row[7]
            }
        return None

    @staticmethod
    def create(car_data):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = '''
            INSERT INTO cars (firm, model, year, power, color, price, dealer_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        '''
        cursor.execute(query, (
            car_data['firm'],
            car_data['model'],
            car_data['year'],
            car_data['power'],
            car_data['color'],
            car_data['price'],
            car_data.get('dealer_id')
        ))

        new_id = cursor.fetchone()[0]
        conn.commit()

        cursor.close()
        conn.close()

        return {**car_data, 'id': new_id}

    @staticmethod
    def update(car_id, car_data):
        conn = get_db_connection()
        cursor = conn.cursor()

        # Проверяем существование
        cursor.execute('SELECT id FROM cars WHERE id = %s', (car_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return None

        query = '''
            UPDATE cars 
            SET firm = %s, model = %s, year = %s, power = %s, 
                color = %s, price = %s, dealer_id = %s
            WHERE id = %s
            RETURNING *
        '''
        cursor.execute(query, (
            car_data['firm'],
            car_data['model'],
            car_data['year'],
            car_data['power'],
            car_data['color'],
            car_data['price'],
            car_data.get('dealer_id'),
            car_id
        ))

        updated_row = cursor.fetchone()
        conn.commit()

        cursor.close()
        conn.close()

        if updated_row:
            return {
                'id': updated_row[0],
                'firm': updated_row[1],
                'model': updated_row[2],
                'year': updated_row[3],
                'power': updated_row[4],
                'color': updated_row[5],
                'price': float(updated_row[6]),
                'dealer_id': updated_row[7]
            }
        return None

    @staticmethod
    def delete(car_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        # Сначала получаем данные автомобиля для события DELETE
        cursor.execute('SELECT * FROM cars WHERE id = %s', (car_id,))
        car_data = cursor.fetchone()

        if not car_data:
            cursor.close()
            conn.close()
            return None

        # Удаляем автомобиль
        cursor.execute('DELETE FROM cars WHERE id = %s', (car_id,))
        conn.commit()

        cursor.close()
        conn.close()

        # Возвращаем данные удаленного автомобиля
        return {
            'id': car_data[0],
            'firm': car_data[1],
            'model': car_data[2],
            'year': car_data[3],
            'power': car_data[4],
            'color': car_data[5],
            'price': float(car_data[6]),
            'dealer_id': car_data[7]
        }