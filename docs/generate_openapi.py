#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, yaml

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app import app


def generate_openapi_yaml() -> None:
    """Создаёт файл docs/openapi.yaml из JSON-спецификации Flasgger."""
    with app.test_client() as client:
        resp = client.get('/apispec_1.json')
        if resp.status_code == 200 and resp.is_json:
            spec = resp.get_json()
            # правим описание
            spec["info"]["title"] = "Телефонный справочник API"
            spec["info"]["description"] = "REST API для управления контактами (РГЗ, вариант 1)."
            # удаляем support/license если есть
            spec["info"].pop("contact", None)
            spec["info"].pop("license", None)
            with open("docs/openapi.yaml", "w", encoding="utf-8") as f:
                yaml.dump(spec, f, allow_unicode=True, default_flow_style=False)
            print("✅ Спецификация OpenAPI сохранена в docs/openapi.yaml")
        else:
            print("❌ Ошибка: не удалось получить спецификацию OpenAPI.")


if __name__ == "__main__":
    generate_openapi_yaml()
