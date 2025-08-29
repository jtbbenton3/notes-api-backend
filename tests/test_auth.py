import json
from app import app, database, User, Note

def setup_module(module):
    # Fresh DB before tests
    database.drop_tables([User, Note])
    database.create_tables([User, Note])

def test_signup_and_login():
    client = app.test_client()

    # signup
    resp = client.post("/signup", json={"username": "testuser", "password": "testpass"})
    assert resp.status_code == 201

    # login
    resp = client.post("/login", json={"username": "testuser", "password": "testpass"})
    assert resp.status_code == 200
    token = resp.get_json()["access_token"]
    assert token