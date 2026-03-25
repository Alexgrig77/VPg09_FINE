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

    def list_users(self, include_admin=True):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if include_admin:
                cursor.execute("""
                    SELECT id, username, full_name, role, is_active, created_at
                    FROM Пользователи
                    ORDER BY role DESC, username
                """)
            else:
                cursor.execute("""
                    SELECT id, username, full_name, role, is_active, created_at
                    FROM Пользователи
                    WHERE role != 'admin'
                    ORDER BY username
                """)
            return [dict(r) for r in cursor.fetchall()]
        finally:
            conn.close()

    def update_user_status(self, user_id, is_active):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE Пользователи SET is_active = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (1 if is_active else 0, user_id),
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def change_user_password(self, user_id, new_password):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE Пользователи SET password_hash = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (generate_password_hash(new_password), user_id),
            )
            conn.commit()
            return cursor.rowcount > 0
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
