"""
Autosalon API package
"""
# Экспортируем только то, что не создает циклических зависимостей
from .db import get_db_connection

__all__ = ['get_db_connection']