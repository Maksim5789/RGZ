#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
РГЗ – Вариант 1.
Flask-приложение (REST API) для управления телефонными контактами.

Основные возможности:
1. POST   /contacts         — создание нового контакта;
2. GET    /contacts/<id>    — получение контакта по идентификатору;
3. DELETE /contacts/<id>    — удаление контакта.
Документация: Swagger UI (Flasgger) — http://127.0.0.1:5000/apidocs
"""

# ---------------------- импорт необходимых библиотек ----------------------
from flask import Flask, jsonify, request, abort, redirect
from flasgger import Swagger, swag_from

# ---------------------- инициализация приложения и Swagger ----------------------
app = Flask(__name__)

# Конфигурация Swagger (отображение в Swagger UI)
swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "Телефонный справочник API",
        "version": "1.0.0",
        "description": "REST API для управления телефонными контактами (РГЗ — вариант 1)."
    }
})

# ---------------------- хранилище данных (оперативная память) ----------------------
# CONTACTS — словарь для хранения контактов.
# NEXT_ID  — счётчик для генерации уникальных идентификаторов.
CONTACTS = {}
NEXT_ID = 1


# =======================================================================
#                    ЭНДПОИНТ 1: СОЗДАНИЕ КОНТАКТА (POST)
# =======================================================================
@swag_from({
    "tags": ["contacts"],
    "description": "Создание нового контакта.",
    "parameters": [{
        "in": "body",
        "name": "payload",
        "required": True,
        "schema": {
            "type": "object",
            "properties": {
                "name":  {"type": "string", "example": "Ivan Petrov"},
                "phone": {"type": "string", "example": "+7-999-123-45-67"}
            },
            "required": ["name", "phone"]
        }
    }],
    "responses": {
        "201": {"description": "Контакт создан успешно"},
        "400": {"description": "Ошибка валидации входных данных"}
    }
})
@app.route("/contacts", methods=["POST"])
def create_contact():
    """
    Создание нового контакта.
    Принимает JSON-объект с полями 'name' и 'phone'.
    Возвращает созданный контакт с присвоенным идентификатором.
    """
    global NEXT_ID
    payload = request.get_json(silent=True) or {}
    name = (payload.get("name") or "").strip()
    phone = (payload.get("phone") or "").strip()

    # Проверка корректности данных
    if not name or not phone:
        abort(400, description="Поле name/phone обязательно.")

    # Генерация идентификатора и сохранение контакта
    cid = NEXT_ID
    NEXT_ID += 1
    CONTACTS[cid] = {"name": name, "phone": phone}

    # Возврат созданного контакта с кодом 201 (Created)
    return jsonify({"id": cid, "name": name, "phone": phone}), 201


# =======================================================================
#              ЭНДПОИНТ 2: ПОЛУЧЕНИЕ КОНТАКТА ПО ID (GET)
# =======================================================================
@swag_from({
    "tags": ["contacts"],
    "description": "Получение контакта по идентификатору.",
    "parameters": [{
        "name": "contact_id",
        "in": "path",
        "required": True,
        "type": "integer",
        "description": "Идентификатор контакта"
    }],
    "responses": {
        "200": {"description": "Контакт найден"},
        "404": {"description": "Контакт не найден"}
    }
})
@app.route("/contacts/<int:contact_id>", methods=["GET"])
def get_contact(contact_id: int):
    """
    Получение информации о контакте по идентификатору.
    Если контакт отсутствует, возвращается ошибка 404.
    """
    contact = CONTACTS.get(contact_id)
    if not contact:
        abort(404, description="Контакт не найден.")

    # Возврат найденного контакта
    return jsonify({"id": contact_id, **contact})


# =======================================================================
#               ЭНДПОИНТ 3: УДАЛЕНИЕ КОНТАКТА ПО ID (DELETE)
# =======================================================================
@swag_from({
    "tags": ["contacts"],
    "description": "Удаление контакта по идентификатору.",
    "parameters": [{
        "name": "contact_id",
        "in": "path",
        "required": True,
        "type": "integer",
        "description": "Идентификатор контакта"
    }],
    "responses": {
        "204": {"description": "Контакт удалён"},
        "404": {"description": "Контакт не найден"}
    }
})
@app.route("/contacts/<int:contact_id>", methods=["DELETE"])
def delete_contact(contact_id: int):
    """
    Удаление контакта по идентификатору.
    Если контакт найден — он удаляется из словаря.
    Возвращает пустой ответ (204 No Content).
    """
    if contact_id not in CONTACTS:
        abort(404, description="Контакт не найден.")
    del CONTACTS[contact_id]
    return ("", 204)


# =======================================================================
#                ДОПОЛНИТЕЛЬНЫЙ МАРШРУТ: РЕДИРЕКТ НА SWAGGER
# =======================================================================
@app.route("/")
def index():
    """
    Перенаправление на страницу Swagger UI (/apidocs).
    Упрощает навигацию при запуске приложения.
    """
    return redirect("/apidocs/")


# =======================================================================
#                       ТОЧКА ВХОДА ПРИ ЗАПУСКЕ
# =======================================================================
if __name__ == "__main__":
    # Запуск Flask-сервера в режиме отладки
    app.run(host="127.0.0.1", port=5000, debug=True)
