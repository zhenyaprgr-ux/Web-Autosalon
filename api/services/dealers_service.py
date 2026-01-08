from api.db import get_db_connection


class DealerService:
    @staticmethod
    def get_all_dealers():
        """Получить всех дилеров"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM dealers ORDER BY id')
        rows = cursor.fetchall()

        result = []
        for row in rows:
            result.append({
                'id': row[0],
                'name': row[1],
                'city': row[2],
                'address': row[3],
                'area': row[4],
                'rating': float(row[5])
            })

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_dealer_by_id(dealer_id):
        """Получить дилера по ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM dealers WHERE id = %s', (dealer_id,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return {
                'id': row[0],
                'name': row[1],
                'city': row[2],
                'address': row[3],
                'area': row[4],
                'rating': float(row[5])
            }
        return None

    @staticmethod
    def get_dealer_cars(dealer_id):
        """Получить автомобили дилера"""
        conn = get_db_connection()
        cursor = conn.cursor()

        # Проверяем существование дилера
        cursor.execute('SELECT id FROM dealers WHERE id = %s', (dealer_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return None

        cursor.execute('SELECT * FROM cars WHERE dealer_id = %s ORDER BY id', (dealer_id,))
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
    def create_dealer(dealer_data):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = '''
            INSERT INTO dealers (name, city, address, area, rating)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        '''
        cursor.execute(query, (
            dealer_data['name'],
            dealer_data['city'],
            dealer_data['address'],
            dealer_data.get('area'),
            dealer_data['rating']
        ))

        new_id = cursor.fetchone()[0]
        conn.commit()

        cursor.close()
        conn.close()

        return {**dealer_data, 'id': new_id}

    @staticmethod
    def update_dealer(dealer_id, dealer_data):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM dealers WHERE id = %s', (dealer_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return None

        query = '''
            UPDATE dealers 
            SET name = %s, city = %s, address = %s, area = %s, rating = %s
            WHERE id = %s
        '''
        cursor.execute(query, (
            dealer_data['name'],
            dealer_data['city'],
            dealer_data['address'],
            dealer_data.get('area'),
            dealer_data['rating'],
            dealer_id
        ))

        conn.commit()
        cursor.close()
        conn.close()
        return {**dealer_data, 'id': dealer_id}

    @staticmethod
    def delete_dealer(dealer_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM dealers WHERE id = %s', (dealer_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return False

        cursor.execute('DELETE FROM dealers WHERE id = %s', (dealer_id,))
        conn.commit()
        cursor.close()
        conn.close()

        return True