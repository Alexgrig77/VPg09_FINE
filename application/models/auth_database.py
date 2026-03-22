#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Модель авторизации"""

import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash


def get_db_path():
    return os.environ.get('DATABASE_PATH', 'data/FISH.db')


class AuthDatabase:
    def __init__(self, db_name=None):
        self.db_name = db_name or get_db_path()

    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def create_auth_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Пользователи (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'user',
                    is_active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка создания таблиц авторизации: {e}")
            return False
        finally:
            conn.close()

    def create_user(self, username, password, full_name, role='user', is_active=True):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Пользователи (username, password_hash, full_name, role, is_active)
                VALUES (?, ?, ?, ?, ?)
            """, (username, generate_password_hash(password), full_name, role, 1 if is_active else 0))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def get_user_by_id(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Пользователи WHERE id = ? AND is_active = 1", (user_id,))
            return cursor.fetchone()
        finally:
            conn.close()

    def get_user_by_username(self, username):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM Пользователи WHERE username = ? AND is_active = 1",
                (username,)
            )
            return cursor.fetchone()
        finally:
            conn.close()

    def verify_password(self, user_row, password):
        if user_row is None:
            return False
        return check_password_hash(user_row['password_hash'], password)
