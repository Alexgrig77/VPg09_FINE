"""Конфигурация приложения FISH-MVP"""
import os
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent


class Config:
    """Базовая конфигурация"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-CHANGE-IN-PRODUCTION'
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or str(BASE_DIR / 'data' / 'FISH.db')
    PERMANENT_SESSION_LIFETIME = timedelta(seconds=int(os.environ.get('SESSION_LIFETIME', 10800)))
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = False

    @staticmethod
    def init_app(app):
        os.makedirs(os.path.dirname(Config.DATABASE_PATH), exist_ok=True)


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
