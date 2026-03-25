#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Flask веб-приложение FISH-MVP — база разрешений на рыболовство"""
VERSION = "1.0.0"

import os
import csv
import io
from flask import (
    Flask, request, jsonify, render_template, session, redirect,
    send_file, make_response
)
from flask_cors import CORS

from config import config
from application.models.fish_database import FishDatabase
from application.models.auth_database import AuthDatabase
from application.utils.decorators import login_required

config_name = os.environ.get('FLASK_ENV', 'development')
app_config = config.get(config_name, config['default'])
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_object(app_config)
app.secret_key = app_config.SECRET_KEY
app_config.init_app(app)
CORS(app)

DB_PATH = app_config.DATABASE_PATH
fish_db = FishDatabase(DB_PATH)
auth_db = AuthDatabase(DB_PATH)


def _current_user():
    if 'user_id' not in session:
        return None
    return auth_db.get_user_by_id(session['user_id'])


def _is_admin(user):
    return bool(user and user['role'] == 'admin')


# --- Auth ---
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '')
    user = auth_db.get_user_by_username(username)
    if not user or not auth_db.verify_password(user, password):
        return jsonify({'error': 'Неверный логин или пароль'}), 401
    session.permanent = True
    session['user_id'] = user['id']
    session['username'] = user['username']
    return jsonify({'ok': True, 'username': user['username'], 'role': user['role']})


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'ok': True})


@app.route('/api/auth/current')
def current_user():
    if 'user_id' not in session:
        return jsonify({'user': None}), 200
    user = _current_user()
    if not user:
        session.clear()
        return jsonify({'user': None}), 200
    return jsonify({'user': {
        'id': user['id'],
        'username': user['username'],
        'role': user['role'],
        'full_name': user['full_name'],
    }})


# --- Admin users ---
@app.route('/api/admin/responsibles')
@login_required
def admin_responsibles():
    user = _current_user()
    if not _is_admin(user):
        return jsonify({'error': 'Доступ запрещен'}), 403
    return jsonify(fish_db.get_responsibles())


@app.route('/api/admin/users', methods=['GET'])
@login_required
def admin_users_list():
    user = _current_user()
    if not _is_admin(user):
        return jsonify({'error': 'Доступ запрещен'}), 403
    return jsonify(auth_db.list_users(include_admin=False))


@app.route('/api/admin/users', methods=['POST'])
@login_required
def admin_users_create():
    user = _current_user()
    if not _is_admin(user):
        return jsonify({'error': 'Доступ запрещен'}), 403
    data = request.get_json() or {}
    username = (data.get('username') or '').strip()
    full_name = (data.get('full_name') or '').strip()
    password = data.get('password') or ''
    if not username or not full_name or not password:
        return jsonify({'error': 'Заполните username, full_name и password'}), 400
    if full_name not in fish_db.get_responsibles():
        return jsonify({'error': 'Сотрудник не найден в таблице Разрешения'}), 400
    ok = auth_db.create_user(username, password, full_name, role='user', is_active=True)
    if not ok:
        return jsonify({'error': 'Пользователь с таким логином уже существует'}), 400
    return jsonify({'ok': True}), 201


@app.route('/api/admin/users/<int:user_id>/password', methods=['PUT'])
@login_required
def admin_change_password(user_id):
    user = _current_user()
    if not _is_admin(user):
        return jsonify({'error': 'Доступ запрещен'}), 403
    data = request.get_json() or {}
    new_password = data.get('password') or ''
    if len(new_password) < 4:
        return jsonify({'error': 'Пароль должен быть не короче 4 символов'}), 400
    ok = auth_db.change_user_password(user_id, new_password)
    if not ok:
        return jsonify({'error': 'Пользователь не найден'}), 404
    return jsonify({'ok': True})


@app.route('/api/admin/users/<int:user_id>/status', methods=['PUT'])
@login_required
def admin_change_status(user_id):
    user = _current_user()
    if not _is_admin(user):
        return jsonify({'error': 'Доступ запрещен'}), 403
    data = request.get_json() or {}
    is_active = bool(data.get('is_active', True))
    ok = auth_db.update_user_status(user_id, is_active)
    if not ok:
        return jsonify({'error': 'Пользователь не найден'}), 404
    return jsonify({'ok': True})


# --- Health (no auth) ---
@app.route('/api/test')
def test_api():
    return jsonify({'status': 'ok', 'version': VERSION})


# --- Permissions ---
@app.route('/api/permissions', methods=['GET'])
@login_required
def list_permissions():
    user = _current_user()
    q = request.args.get('q', '')
    responsible = None if _is_admin(user) else user['full_name']
    items = fish_db.get_all_permissions(q or None, responsible=responsible)
    return jsonify(items)


@app.route('/api/permissions/<int:pk>', methods=['GET'])
@login_required
def get_permission(pk):
    user = _current_user()
    item = fish_db.get_permission(pk)
    if not item:
        return jsonify({'error': 'Не найдено'}), 404
    if not _is_admin(user) and item.get('Ответственный') != user['full_name']:
        return jsonify({'error': 'Доступ запрещен'}), 403
    return jsonify(item)


@app.route('/api/permissions', methods=['POST'])
@login_required
def create_permission():
    user = _current_user()
    if not _is_admin(user):
        return jsonify({'error': 'Доступ запрещен'}), 403
    data = request.get_json() or {}
    try:
        pid = fish_db.create_permission(data)
        return jsonify({'id': pid}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/permissions/<int:pk>', methods=['PUT'])
@login_required
def update_permission(pk):
    user = _current_user()
    if not _is_admin(user):
        return jsonify({'error': 'Доступ запрещен'}), 403
    data = request.get_json() or {}
    ok = fish_db.update_permission(pk, data)
    if not ok:
        return jsonify({'error': 'Не найдено'}), 404
    return jsonify({'ok': True})


@app.route('/api/permissions/<int:pk>', methods=['DELETE'])
@login_required
def delete_permission(pk):
    user = _current_user()
    if not _is_admin(user):
        return jsonify({'error': 'Доступ запрещен'}), 403
    ok = fish_db.delete_permission(pk)
    if not ok:
        return jsonify({'error': 'Не найдено'}), 404
    return jsonify({'ok': True})


# --- Fish ---
@app.route('/api/fish', methods=['GET'])
@login_required
def list_fish():
    q = request.args.get('q', '')
    items = fish_db.get_all_fish(q or None)
    return jsonify(items)


@app.route('/api/fish/<int:pk>', methods=['GET'])
@login_required
def get_fish(pk):
    item = fish_db.get_fish(pk)
    if not item:
        return jsonify({'error': 'Не найдено'}), 404
    return jsonify(item)


@app.route('/api/fish', methods=['POST'])
@login_required
def create_fish():
    user = _current_user()
    if not _is_admin(user):
        return jsonify({'error': 'Доступ запрещен'}), 403
    data = request.get_json() or {}
    try:
        fid = fish_db.create_fish(data)
        return jsonify({'id': fid}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/fish/<int:pk>', methods=['PUT'])
@login_required
def update_fish(pk):
    user = _current_user()
    if not _is_admin(user):
        return jsonify({'error': 'Доступ запрещен'}), 403
    data = request.get_json() or {}
    ok = fish_db.update_fish(pk, data)
    if not ok:
        return jsonify({'error': 'Не найдено'}), 404
    return jsonify({'ok': True})


@app.route('/api/fish/<int:pk>', methods=['DELETE'])
@login_required
def delete_fish(pk):
    user = _current_user()
    if not _is_admin(user):
        return jsonify({'error': 'Доступ запрещен'}), 403
    ok = fish_db.delete_fish(pk)
    if not ok:
        return jsonify({'error': 'Не найдено'}), 404
    return jsonify({'ok': True})


# --- Catches ---
@app.route('/api/catches', methods=['GET'])
@login_required
def list_catches():
    user = _current_user()
    perm = request.args.get('permission', '')
    fish = request.args.get('fish', '')
    responsible = None if _is_admin(user) else user['full_name']
    items = fish_db.get_all_catches(perm or None, fish or None, responsible=responsible)
    return jsonify(items)


@app.route('/api/catches/<int:pk>', methods=['GET'])
@login_required
def get_catch(pk):
    user = _current_user()
    item = fish_db.get_catch(pk)
    if not item:
        return jsonify({'error': 'Не найдено'}), 404
    if not _is_admin(user):
        has_access = fish_db.has_permission_for_responsible(item.get('Разрешение', ''), user['full_name'])
        if not has_access:
            return jsonify({'error': 'Доступ запрещен'}), 403
    return jsonify(item)


@app.route('/api/catches', methods=['POST'])
@login_required
def create_catch():
    user = _current_user()
    data = request.get_json() or {}
    if not _is_admin(user):
        permission_number = data.get('Разрешение', '')
        if not fish_db.has_permission_for_responsible(permission_number, user['full_name']):
            return jsonify({'error': 'Можно добавлять вылов только по своим разрешениям'}), 403
    try:
        cid = fish_db.create_catch(data)
        return jsonify({'id': cid}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/catches/<int:pk>', methods=['PUT'])
@login_required
def update_catch(pk):
    user = _current_user()
    if not _is_admin(user):
        return jsonify({'error': 'Доступ запрещен'}), 403
    data = request.get_json() or {}
    ok = fish_db.update_catch(pk, data)
    if not ok:
        return jsonify({'error': 'Не найдено'}), 404
    return jsonify({'ok': True})


@app.route('/api/catches/<int:pk>', methods=['DELETE'])
@login_required
def delete_catch(pk):
    user = _current_user()
    if not _is_admin(user):
        return jsonify({'error': 'Доступ запрещен'}), 403
    ok = fish_db.delete_catch(pk)
    if not ok:
        return jsonify({'error': 'Не найдено'}), 404
    return jsonify({'ok': True})


# --- Stats & Export ---
@app.route('/api/statistics')
@login_required
def statistics():
    user = _current_user()
    responsible = None if _is_admin(user) else user['full_name']
    return jsonify(fish_db.get_statistics(responsible=responsible))


@app.route('/api/export-catches')
@login_required
def export_catches():
    user = _current_user()
    responsible = None if _is_admin(user) else user['full_name']
    items = fish_db.get_all_catches(responsible=responsible)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Разрешение', 'Дата_вылова', 'Наименование_рыбы', 'Количество', 'Сумма'])
    for r in items:
        writer.writerow([
            r.get('Разрешение', ''),
            r.get('Дата_вылова', ''),
            r.get('Наименование_рыбы', ''),
            r.get('Количество', 0),
            r.get('Сумма', 0)
        ])
    resp = make_response(output.getvalue())
    resp.headers['Content-Type'] = 'text/csv; charset=utf-8'
    resp.headers['Content-Disposition'] = 'attachment; filename=catches.csv'
    return resp


@app.route('/api/permission-numbers')
@login_required
def permission_numbers():
    user = _current_user()
    responsible = None if _is_admin(user) else user['full_name']
    return jsonify(fish_db.get_permission_numbers(responsible=responsible))


@app.route('/api/fish-names')
@login_required
def fish_names():
    return jsonify(fish_db.get_fish_names())


# --- Pages ---
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login.html')
    return render_template('index.html')


@app.route('/login.html')
def login_page():
    return render_template('login.html')


@app.route('/permissions.html')
@login_required
def permissions_page():
    return render_template('permissions.html')


@app.route('/fish.html')
@login_required
def fish_page():
    return render_template('fish.html')


@app.route('/catches.html')
@login_required
def catches_page():
    return render_template('catches.html')


@app.route('/statistics.html')
@login_required
def statistics_page():
    return render_template('statistics.html')


@app.route('/admin-users.html')
@login_required
def admin_users_page():
    user = _current_user()
    if not _is_admin(user):
        return redirect('/')
    return render_template('admin-users.html')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=app_config.DEBUG)
