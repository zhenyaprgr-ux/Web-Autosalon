from api.repositories.car_repository import CarRepository


class CarService:


    @staticmethod
    def get_all_cars():
        return CarRepository.get_all()

    @staticmethod
    def get_car_by_id(car_id):
        return CarRepository.get_by_id(car_id)

    @staticmethod
    def create_car(car_data):
        # Можно добавить бизнес-логику перед сохранением
        if car_data['price'] <= 0:
            raise ValueError("Цена должна быть положительной")
        if car_data['year'] < 1900 or car_data['year'] > 2025:
            raise ValueError("Некорректный год выпуска")

        return CarRepository.create(car_data)

    @staticmethod
    def update_car(car_id, car_data):
        # Бизнес-логика
        if 'price' in car_data and car_data['price'] <= 0:
            raise ValueError("Цена должна быть положительной")

        return CarRepository.update(car_id, car_data)

    @staticmethod
    def delete_car(car_id):
        return CarRepository.delete(car_id)

