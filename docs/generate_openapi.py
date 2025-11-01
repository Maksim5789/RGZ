#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import yaml
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app import app

def generate_openapi_yaml():
    """Извлекает JSON-спецификацию Flasgger и сохраняет в docs/openapi.yaml."""
    with app.test_client() as client:
        resp = client.get('/apispec_1.json')
        if resp.status_code == 200 and resp.is_json:
            spec = resp.get_json()
            os.makedirs("docs", exist_ok=True)
            with open("docs/openapi.yaml", "w", encoding="utf-8") as f:
                yaml.dump(spec, f, allow_unicode=True, default_flow_style=False)
            print("✅ Спецификация OpenAPI сохранена в docs/openapi.yaml")
        else:
            print("❌ Ошибка: не удалось получить спецификацию OpenAPI.")

if __name__ == "__main__":
    generate_openapi_yaml()
