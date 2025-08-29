# tests/conftest.py
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app, bcrypt
from models import database, User, Note

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

@pytest.fixture
def token(client):
    # reset DB
    with database.atomic():
        Note.delete().execute()
        User.delete().execute()
        u = User.create(username="testuser", password_hash="")
        u.set_password(bcrypt, "testpass")
        u.save()

    resp = client.post("/login", json={"username": "testuser", "password": "testpass"})
    return resp.get_json()["access_token"]