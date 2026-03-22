"""Декораторы для проверки авторизации"""
from functools import wraps
from flask import session, redirect, url_for, jsonify, request
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
DB_PATH = os.environ.get('DATABASE_PATH') or str(BASE_DIR / 'data' / 'FISH.db')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.path.startswith('/api/'):
                return jsonify({'error': 'Требуется авторизация', 'redirect': '/login.html'}), 401
            return redirect('/login.html')
        return f(*args, **kwargs)
    return decorated_function
