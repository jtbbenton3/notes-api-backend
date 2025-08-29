# Notes API Backend

A simple Flask + SQLite backend for a Notes app with **JWT authentication**, **bcrypt-hashed passwords**, and full **CRUD** for notes. All note routes are **protected** so each user only sees and edits their own notes. The list endpoint supports **pagination**.

---

## Features
- User signup, login, and “me” (current user) endpoints
- Passwords hashed with bcrypt (no raw passwords stored)
- JWT auth protecting all notes routes
- Notes CRUD (create/read/update/delete)
- Paginated `GET /notes?page=1&per_page=10`
- SQLite database for easy local setup
- Seed script for quick demo data

## Tech Stack
- Python 3.8
- Flask, flask-jwt-extended, flask-bcrypt
- Peewee ORM (SQLite)
- Marshmallow for request/response schemas

---

## Requirements
- Python **3.8**
- `pip` and `pipenv` (`pip install pipenv`)

## Installation
```bash
pip install pipenv
pipenv install
pipenv shell