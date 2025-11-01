#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
РГЗ — Вариант 1.
Тема: Разработка Flask-приложения (REST API) для управления телефонными контактами.

ФУНКЦИОНАЛ:
1) POST /contacts           — создание контакта.
2) GET  /contacts/<id>      — получение контакта по идентификатору.
3) DELETE /contacts/<id>    — удаление контакта по идентификатору.

ОСОБЕННОСТИ:
- Хранилище: оперативная память (in-memory словарь). Данные не сохраняются между перезапусками.
- Документация: Flasgger (Swagger UI и OpenAPI JSON).
- Валидация: проверяются обязательные поля и их типы.
- Коды ответов: 201 (создано), 200 (успех), 204 (удалено), 400 (ошибка входных данных), 404 (не найдено).
"""

from __future__ import annotations
from typing import Dict, Any

from flask import Flask, jsonify, request, abort
from flasgger import Swagger

# ---------------------------------------------------------------------------
# 1. Инициализация веб-приложения и документации
# ---------------------------------------------------------------------------
app = Flask(__name__)
# Swagger инициализируется "как есть": /apidocs — UI, /apispec_1.json — OpenAPI JSON
swagger = Swagger(app)

# ---------------------------------------------------------------------------
# 2. Простейшее хранилище данных (in-memory)
#    Ключ: int (идентификатор контакта)
#    Значение: dict с полями 'name' (str), 'phone' (str)
#    ВНИМАНИЕ: при перезапуске приложения данные будут потеряны — для РГЗ достаточно.
# ---------------------------------------------------------------------------
CONTACTS: Dict[int, Dict[str, Any]] = {}
NEXT_ID: int = 1  # счётчик идентификаторов (монотонный, только наращивается)


def _validate_contact_payload(payload: Dict[str, Any]) -> None:
    """
    Формальная проверка структуры входных данных при создании контакта.

    Требования к телу запроса (JSON-объект):
      - Поле "name": обязательная непустая строка.
      - Поле "phone": обязательная непустая строка.

    В случае нарушения требований возбуждается HTTP 400 (Bad Request).
    """
    if not isinstance(payload, dict):
        abort(400, description="Тело запроса должно быть JSON-объектом.")
    for field in ("name", "phone"):
        if field not in payload:
            abort(400, description=f"Отсутствует обязательное поле: {field}.")
        if not isinstance(payload[field], str) or not payload[field].strip():
            abort(400, description=f"Поле {field} должно быть непустой строкой.")


# ---------------------------------------------------------------------------
# 3. Эндпоинты API
# ---------------------------------------------------------------------------
@app.post("/contacts")
def create_contact():
    """
    Создание нового контакта.
    ---
    tags:
      - contacts
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
                example: "Ivan Petrov"
              phone:
                type: string
                example: "+7-999-123-45-67"
            required: [name, phone]
    responses:
      201:
        description: Контакт создан успешно
        content:
          application/json:
            schema:
              type: object
              properties:
                id:    {type: integer, example: 1}
                name:  {type: string}
                phone: {type: string}
      400:
        description: Ошибка валидации входных данных
    """
    global NEXT_ID

    payload = request.get_json(silent=True)
    _validate_contact_payload(payload)

    contact_id = NEXT_ID
    NEXT_ID += 1

    CONTACTS[contact_id] = {
        "name": payload["name"].strip(),
        "phone": payload["phone"].strip()
    }
    # Возвращаем созданный ресурс и код 201
    return jsonify({"id": contact_id, **CONTACTS[contact_id]}), 201


@app.get("/contacts/<int:contact_id>")
def get_contact(contact_id: int):
    """
    Получение контакта по идентификатору.
    ---
    tags:
      - contacts
    parameters:
      - name: contact_id
        in: path
        required: true
        schema: {type: integer}
        description: Идентификатор контакта
    responses:
      200:
        description: Контакт найден
        content:
          application/json:
            schema:
              type: object
              properties:
                id:    {type: integer}
                name:  {type: string}
                phone: {type: string}
      404:
        description: Контакт не найден
    """
    contact = CONTACTS.get(contact_id)
    if not contact:
        abort(404, description="Контакт не найден.")
    return jsonify({"id": contact_id, **contact})


@app.delete("/contacts/<int:contact_id>")
def delete_contact(contact_id: int):
    """
    Удаление контакта по идентификатору.
    ---
    tags:
      - contacts
    parameters:
      - name: contact_id
        in: path
        required: true
        schema: {type: integer}
        description: Идентификатор контакта
    responses:
      204:
        description: Удаление выполнено (без тела ответа)
      404:
        description: Контакт не найден
    """
    if contact_id not in CONTACTS:
        abort(404, description="Контакт не найден.")
    del CONTACTS[contact_id]
    # Стандарт: 204 No Content — пустой ответ при успешном удалении.
    return ("", 204)


# ---------------------------------------------------------------------------
# 4. Точка входа
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Разработческая конфигурация: localhost:5000, включён debug для удобства в РГЗ
    app.run(host="127.0.0.1", port=5000, debug=True)
