#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Модель БД для разрешений, рыбы и выловов"""

import sqlite3
import os
from datetime import datetime


def get_db_path():
    return os.environ.get('DATABASE_PATH', 'data/FISH.db')


class FishDatabase:
    def __init__(self, db_name=None):
        self.db_name = db_name or get_db_path()

    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Разрешения (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Номер_разрешения TEXT NOT NULL,
                    Год TEXT NOT NULL,
                    Район_промысла TEXT,
                    Ответственный TEXT,
                    Наименование_групповое TEXT,
                    Лимит_кг INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Рыба (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Наименование_рыбы TEXT NOT NULL,
                    Наименование_групповое TEXT,
                    Цена REAL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Выловы (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Разрешение TEXT NOT NULL,
                    Дата_вылова DATE NOT NULL,
                    Наименование_рыбы TEXT NOT NULL,
                    Количество INTEGER NOT NULL,
                    Сумма REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка создания таблиц: {e}")
            return False
        finally:
            conn.close()

    def get_all_permissions(self, search=None, responsible=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if search and responsible:
                cursor.execute("""
                    SELECT * FROM Разрешения
                    WHERE (Номер_разрешения LIKE ? OR Район_промысла LIKE ? OR Ответственный LIKE ? OR Наименование_групповое LIKE ?)
                    AND Ответственный = ?
                    ORDER BY id DESC
                """, (f'%{search}%', f'%{search}%', f'%{search}%', f'%{search}%', responsible))
            elif search:
                cursor.execute("""
                    SELECT * FROM Разрешения WHERE Номер_разрешения LIKE ? OR Район_промысла LIKE ?
                    OR Ответственный LIKE ? OR Наименование_групповое LIKE ?
                    ORDER BY id DESC
                """, (f'%{search}%', f'%{search}%', f'%{search}%', f'%{search}%'))
            elif responsible:
                cursor.execute("SELECT * FROM Разрешения WHERE Ответственный = ? ORDER BY id DESC", (responsible,))
            else:
                cursor.execute("SELECT * FROM Разрешения ORDER BY id DESC")
            return [dict(r) for r in cursor.fetchall()]
        finally:
            conn.close()

    def get_permission(self, pk):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Разрешения WHERE id = ?", (pk,))
            r = cursor.fetchone()
            return dict(r) if r else None
        finally:
            conn.close()

    def create_permission(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Разрешения (Номер_разрешения, Год, Район_промысла, Ответственный,
                Наименование_групповое, Лимит_кг, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                data.get('Номер_разрешения', ''),
                data.get('Год', ''),
                data.get('Район_промысла', ''),
                data.get('Ответственный', ''),
                data.get('Наименование_групповое', ''),
                data.get('Лимит_кг') or 0
            ))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            raise ValueError(str(e))
        finally:
            conn.close()

    def update_permission(self, pk, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE Разрешения SET Номер_разрешения=?, Год=?, Район_промысла=?,
                Ответственный=?, Наименование_групповое=?, Лимит_кг=?, updated_at=CURRENT_TIMESTAMP
                WHERE id=?
            """, (
                data.get('Номер_разрешения', ''),
                data.get('Год', ''),
                data.get('Район_промысла', ''),
                data.get('Ответственный', ''),
                data.get('Наименование_групповое', ''),
                data.get('Лимит_кг') or 0,
                pk
            ))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def delete_permission(self, pk):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Разрешения WHERE id = ?", (pk,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def get_all_fish(self, search=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if search:
                cursor.execute("""
                    SELECT * FROM Рыба WHERE Наименование_рыбы LIKE ? OR Наименование_групповое LIKE ?
                    ORDER BY id DESC
                """, (f'%{search}%', f'%{search}%'))
            else:
                cursor.execute("SELECT * FROM Рыба ORDER BY id DESC")
            return [dict(r) for r in cursor.fetchall()]
        finally:
            conn.close()

    def get_fish(self, pk):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Рыба WHERE id = ?", (pk,))
            r = cursor.fetchone()
            return dict(r) if r else None
        finally:
            conn.close()

    def get_fish_price(self, name):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT Цена FROM Рыба WHERE Наименование_рыбы = ?", (name,))
            r = cursor.fetchone()
            return float(r['Цена']) if r and r['Цена'] else 0.0
        finally:
            conn.close()

    def create_fish(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Рыба (Наименование_рыбы, Наименование_групповое, Цена, updated_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                data.get('Наименование_рыбы', ''),
                data.get('Наименование_групповое', ''),
                float(data.get('Цена', 0) or 0)
            ))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            raise ValueError(str(e))
        finally:
            conn.close()

    def update_fish(self, pk, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE Рыба SET Наименование_рыбы=?, Наименование_групповое=?, Цена=?, updated_at=CURRENT_TIMESTAMP
                WHERE id=?
            """, (
                data.get('Наименование_рыбы', ''),
                data.get('Наименование_групповое', ''),
                float(data.get('Цена', 0) or 0),
                pk
            ))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def delete_fish(self, pk):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Рыба WHERE id = ?", (pk,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def get_all_catches(self, permission=None, fish=None, responsible=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if responsible:
                base = """
                    SELECT * FROM Выловы
                    WHERE Разрешение IN (
                        SELECT Номер_разрешения FROM Разрешения WHERE Ответственный = ?
                    )
                """
                params = [responsible]
                if permission:
                    base += " AND Разрешение = ?"
                    params.append(permission)
                if fish:
                    base += " AND Наименование_рыбы = ?"
                    params.append(fish)
                base += " ORDER BY id DESC"
                cursor.execute(base, tuple(params))
            elif permission:
                cursor.execute("SELECT * FROM Выловы WHERE Разрешение = ? ORDER BY id DESC", (permission,))
            elif fish:
                cursor.execute("SELECT * FROM Выловы WHERE Наименование_рыбы = ? ORDER BY id DESC", (fish,))
            else:
                cursor.execute("SELECT * FROM Выловы ORDER BY id DESC")
            return [dict(r) for r in cursor.fetchall()]
        finally:
            conn.close()

    def get_catch(self, pk):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Выловы WHERE id = ?", (pk,))
            r = cursor.fetchone()
            return dict(r) if r else None
        finally:
            conn.close()

    def create_catch(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            price = self.get_fish_price(data.get('Наименование_рыбы', ''))
            qty = int(data.get('Количество', 0) or 0)
            total = round(price * qty, 2)
            cursor.execute("""
                INSERT INTO Выловы (Разрешение, Дата_вылова, Наименование_рыбы, Количество, Сумма, updated_at)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                data.get('Разрешение', ''),
                data.get('Дата_вылова', ''),
                data.get('Наименование_рыбы', ''),
                qty,
                total
            ))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            raise ValueError(str(e))
        finally:
            conn.close()

    def update_catch(self, pk, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            price = self.get_fish_price(data.get('Наименование_рыбы', ''))
            qty = int(data.get('Количество', 0) or 0)
            total = round(price * qty, 2)
            cursor.execute("""
                UPDATE Выловы SET Разрешение=?, Дата_вылова=?, Наименование_рыбы=?, Количество=?, Сумма=?, updated_at=CURRENT_TIMESTAMP
                WHERE id=?
            """, (
                data.get('Разрешение', ''),
                data.get('Дата_вылова', ''),
                data.get('Наименование_рыбы', ''),
                qty,
                total,
                pk
            ))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def delete_catch(self, pk):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Выловы WHERE id = ?", (pk,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def get_statistics(self, responsible=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if responsible:
                cursor.execute("""
                    SELECT COUNT(*) as cnt, COALESCE(SUM(Сумма), 0) as total
                    FROM Выловы
                    WHERE Разрешение IN (
                        SELECT Номер_разрешения FROM Разрешения WHERE Ответственный = ?
                    )
                """, (responsible,))
            else:
                cursor.execute("SELECT COUNT(*) as cnt, COALESCE(SUM(Сумма), 0) as total FROM Выловы")
            r = cursor.fetchone()
            if responsible:
                cursor.execute("""
                    SELECT Разрешение, COUNT(*) as cnt, COALESCE(SUM(Сумма), 0) as total
                    FROM Выловы
                    WHERE Разрешение IN (
                        SELECT Номер_разрешения FROM Разрешения WHERE Ответственный = ?
                    )
                    GROUP BY Разрешение
                """, (responsible,))
            else:
                cursor.execute("""
                    SELECT Разрешение, COUNT(*) as cnt, COALESCE(SUM(Сумма), 0) as total
                    FROM Выловы GROUP BY Разрешение
                """)
            by_perm = [dict(row) for row in cursor.fetchall()]
            return {
                'total_catches': r['cnt'] or 0,
                'total_sum': float(r['total'] or 0),
                'by_permission': by_perm
            }
        finally:
            conn.close()

    def get_permission_numbers(self, responsible=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if responsible:
                cursor.execute("""
                    SELECT DISTINCT Номер_разрешения FROM Разрешения
                    WHERE Ответственный = ?
                    ORDER BY Номер_разрешения
                """, (responsible,))
            else:
                cursor.execute("SELECT DISTINCT Номер_разрешения FROM Разрешения ORDER BY Номер_разрешения")
            return [r['Номер_разрешения'] for r in cursor.fetchall()]
        finally:
            conn.close()

    def get_fish_names(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT DISTINCT Наименование_рыбы FROM Рыба ORDER BY Наименование_рыбы")
            return [r['Наименование_рыбы'] for r in cursor.fetchall()]
        finally:
            conn.close()

    def get_fish_names_by_permission(self, permission_number, responsible=None):
        """
        Вернуть список названий рыбы, доступных для выбранного разрешения.
        В MVP логика такая: разрешение имеет `Наименование_групповое`, а в таблице `Рыба`
        есть `Наименование_групповое`. Берём рыбу, у которой группа совпадает с группой разрешения.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # 1) Забираем "группы" рыбы из разрешения
            if responsible:
                cursor.execute(
                    """
                    SELECT DISTINCT TRIM(Наименование_групповое) AS g
                    FROM Разрешения
                    WHERE Номер_разрешения = ?
                      AND Ответственный = ?
                      AND Наименование_групповое IS NOT NULL
                      AND TRIM(Наименование_групповое) != ''
                    """,
                    (permission_number, responsible),
                )
            else:
                cursor.execute(
                    """
                    SELECT DISTINCT TRIM(Наименование_групповое) AS g
                    FROM Разрешения
                    WHERE Номер_разрешения = ?
                      AND Наименование_групповое IS NOT NULL
                      AND TRIM(Наименование_групповое) != ''
                    """,
                    (permission_number,),
                )

            perm_groups = [r['g'] for r in cursor.fetchall() if r['g']]
            if not perm_groups:
                return []

            # 2) Пытаемся найти рыбу в справочнике Рыба по совпадению группы
            placeholders = ','.join('?' * len(perm_groups))
            cursor.execute(
                f"""
                SELECT DISTINCT TRIM(Наименование_рыбы) AS name
                FROM Рыба
                WHERE TRIM(Наименование_групповое) IN ({placeholders})
                ORDER BY name
                """,
                tuple(perm_groups),
            )
            fish_names = [r['name'] for r in cursor.fetchall() if r['name']]

            # 3) Если в справочнике Рыба нет соответствий (например, разрешение заполнено,
            # а Рыба пока не содержит нужных записей) — используем группы разрешения как fallback.
            return fish_names if fish_names else perm_groups
        finally:
            conn.close()

    def get_responsibles(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT DISTINCT TRIM(Ответственный) AS Ответственный
                FROM Разрешения
                WHERE Ответственный IS NOT NULL AND TRIM(Ответственный) != ''
                ORDER BY Ответственный
            """)
            return [r['Ответственный'] for r in cursor.fetchall()]
        finally:
            conn.close()

    def has_permission_for_responsible(self, permission_number, responsible):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT 1 FROM Разрешения
                WHERE Номер_разрешения = ? AND Ответственный = ?
                LIMIT 1
            """, (permission_number, responsible))
            return cursor.fetchone() is not None
        finally:
            conn.close()
