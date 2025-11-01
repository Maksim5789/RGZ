#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
РГЗ — Вариант 1.
Скрипт генерации спецификации OpenAPI (формат YAML) на основе JSON-документа,
создаваемого библиотекой Flasgger из Flask-приложения.

Назначение:
- Извлекает описание API (endpoints, схемы, параметры) из работающего Flask-приложения.
- Сохраняет спецификацию в файл docs/openapi.yaml для дальнейшей публикации через ReDoc.
"""

import yaml
import sys
import os

# Добавление корневой директории проекта в путь поиска модулей
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Импорт Flask-приложения (объект app)
from app import app


def generate_openapi_yaml():
    """
    Извлекает JSON-спецификацию Flasgger и сохраняет её в формате OpenAPI YAML.
    Формирует файл docs/openapi.yaml, который используется для публикации на GitHub Pages.
    """
    with app.test_client() as client:
        # Получение JSON-версии спецификации (автоматически генерируется Flasgger)
        resp = client.get('/apispec_1.json')

        # Проверка успешного получения спецификации
        if resp.status_code == 200 and resp.is_json:
            spec = resp.get_json()

            # Создание директории docs, если отсутствует
            os.makedirs("docs", exist_ok=True)

            # Сохранение спецификации в формате YAML
            with open("docs/openapi.yaml", "w", encoding="utf-8") as f:
                yaml.dump(spec, f, allow_unicode=True, default_flow_style=False)

            print("✅ Спецификация OpenAPI сохранена в docs/openapi.yaml")
        else:
            print("❌ Ошибка: не удалось получить спецификацию OpenAPI.")


# Точка входа
if __name__ == "__main__":
    generate_openapi_yaml()
