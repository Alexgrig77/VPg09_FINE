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
    user = auth_db.get_user_by_id(session['user_id'])
    if not user:
        session.clear()
        return jsonify({'user': None}), 200
    return jsonify({'user': {'id': user['id'], 'username': user['username'], 'role': user['role']}})


# --- Health (no auth) ---
@app.route('/api/test')
def test_api():
    return jsonify({'status': 'ok', 'version': VERSION})


# --- Permissions ---
@app.route('/api/permissions', methods=['GET'])
@login_required
def list_permissions():
    q = request.args.get('q', '')
    items = fish_db.get_all_permissions(q or None)
    return jsonify(items)


@app.route('/api/permissions/<int:pk>', methods=['GET'])
@login_required
def get_permission(pk):
    item = fish_db.get_permission(pk)
    if not item:
        return jsonify({'error': 'Не найдено'}), 404
    return jsonify(item)


@app.route('/api/permissions', methods=['POST'])
@login_required
def create_permission():
    data = request.get_json() or {}
    try:
        pid = fish_db.create_permission(data)
        return jsonify({'id': pid}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/permissions/<int:pk>', methods=['PUT'])
@login_required
def update_permission(pk):
    data = request.get_json() or {}
    ok = fish_db.update_permission(pk, data)
    if not ok:
        return jsonify({'error': 'Не найдено'}), 404
    return jsonify({'ok': True})


@app.route('/api/permissions/<int:pk>', methods=['DELETE'])
@login_required
def delete_permission(pk):
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
    data = request.get_json() or {}
    try:
        fid = fish_db.create_fish(data)
        return jsonify({'id': fid}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/fish/<int:pk>', methods=['PUT'])
@login_required
def update_fish(pk):
    data = request.get_json() or {}
    ok = fish_db.update_fish(pk, data)
    if not ok:
        return jsonify({'error': 'Не найдено'}), 404
    return jsonify({'ok': True})


@app.route('/api/fish/<int:pk>', methods=['DELETE'])
@login_required
def delete_fish(pk):
    ok = fish_db.delete_fish(pk)
    if not ok:
        return jsonify({'error': 'Не найдено'}), 404
    return jsonify({'ok': True})


# --- Catches ---
@app.route('/api/catches', methods=['GET'])
@login_required
def list_catches():
    perm = request.args.get('permission', '')
    fish = request.args.get('fish', '')
    items = fish_db.get_all_catches(perm or None, fish or None)
    return jsonify(items)


@app.route('/api/catches/<int:pk>', methods=['GET'])
@login_required
def get_catch(pk):
    item = fish_db.get_catch(pk)
    if not item:
        return jsonify({'error': 'Не найдено'}), 404
    return jsonify(item)


@app.route('/api/catches', methods=['POST'])
@login_required
def create_catch():
    data = request.get_json() or {}
    try:
        cid = fish_db.create_catch(data)
        return jsonify({'id': cid}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/catches/<int:pk>', methods=['PUT'])
@login_required
def update_catch(pk):
    data = request.get_json() or {}
    ok = fish_db.update_catch(pk, data)
    if not ok:
        return jsonify({'error': 'Не найдено'}), 404
    return jsonify({'ok': True})


@app.route('/api/catches/<int:pk>', methods=['DELETE'])
@login_required
def delete_catch(pk):
    ok = fish_db.delete_catch(pk)
    if not ok:
        return jsonify({'error': 'Не найдено'}), 404
    return jsonify({'ok': True})


# --- Stats & Export ---
@app.route('/api/statistics')
@login_required
def statistics():
    return jsonify(fish_db.get_statistics())


@app.route('/api/export-catches')
@login_required
def export_catches():
    items = fish_db.get_all_catches()
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
    return jsonify(fish_db.get_permission_numbers())


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




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=app_config.DEBUG)
