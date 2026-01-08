from api.db import get_db_connection


class CarService:
    @staticmethod
    def get_all_cars():
        """Получить все автомобили"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cars ORDER BY id')
        rows = cursor.fetchall()

        result = []
        for row in rows:
            result.append({
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
        return result

    @staticmethod
    def get_car_by_id(car_id):
        """Получить автомобиль по ID"""
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
    def create_car(car_data):
        """Создать новый автомобиль"""
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
    def update_car(car_id, car_data):
        conn = get_db_connection()
        cursor = conn.cursor()
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

        conn.commit()

        cursor.close()
        conn.close()

        return {**car_data, 'id': car_id}

    @staticmethod
    def delete_car(car_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        # Проверяем существование
        cursor.execute('SELECT id FROM cars WHERE id = %s', (car_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return False

        cursor.execute('DELETE FROM cars WHERE id = %s', (car_id,))
        conn.commit()

        cursor.close()
        conn.close()

        return True