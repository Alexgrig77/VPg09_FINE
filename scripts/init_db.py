#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Инициализация БД FISH-MVP"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from application.models.fish_database import FishDatabase
from application.models.auth_database import AuthDatabase


def main():
    db_path = os.environ.get('DATABASE_PATH', 'data/FISH.db')
    os.makedirs(os.path.dirname(db_path) or '.', exist_ok=True)

    fd = FishDatabase(db_path)
    fd.create_tables()
    print("Таблицы Разрешения, Рыба, Выловы созданы")

    ad = AuthDatabase(db_path)
    ad.create_auth_tables()
    print("Таблица Пользователи создана")

    if ad.get_user_by_username('admin') is None:
        ad.create_user('admin', 'admin123', 'Администратор', 'admin')
        print("Создан пользователь admin / admin123")
    else:
        print("Пользователь admin уже существует")

    print("БД инициализирована")


if __name__ == '__main__':
    main()
