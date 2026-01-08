"""
Controllers package
"""
# Экспортируем функции регистрации для удобного импорта
from .cars_controller import register_cars_routes
from .dealers_controller import register_dealers_routes

__all__ = ['register_cars_routes', 'register_dealers_routes']