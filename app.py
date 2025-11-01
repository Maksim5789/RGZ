#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
РГЗ – Вариант 1.
Flask-приложение (REST API) для управления телефонными контактами.
"""

from flask import Flask, jsonify, request, abort, redirect
from flasgger import Swagger, swag_from

app = Flask(__name__)

swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "Телефонный справочник API",
        "version": "1.0.0",
        "description": "REST API для управления телефонными контактами (РГЗ — вариант 1)."
    }
})

# --- хранилище данных ---
CONTACTS = {}
NEXT_ID = 1


# ---------- POST /contacts ----------
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
    global NEXT_ID
    payload = request.get_json(silent=True) or {}
    name = (payload.get("name") or "").strip()
    phone = (payload.get("phone") or "").strip()
    if not name or not phone:
        abort(400, description="Поле name/phone обязательно.")
    cid = NEXT_ID
    NEXT_ID += 1
    CONTACTS[cid] = {"name": name, "phone": phone}
    return jsonify({"id": cid, "name": name, "phone": phone}), 201


# ---------- GET /contacts/<id> ----------
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
    contact = CONTACTS.get(contact_id)
    if not contact:
        abort(404, description="Контакт не найден.")
    return jsonify({"id": contact_id, **contact})


# ---------- DELETE /contacts/<id> ----------
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
    if contact_id not in CONTACTS:
        abort(404, description="Контакт не найден.")
    del CONTACTS[contact_id]
    return ("", 204)


# ---------- редирект на Swagger UI ----------
@app.route("/")
def index():
    return redirect("/apidocs/")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
