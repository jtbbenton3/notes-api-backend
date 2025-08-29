import json
from app import app

def test_notes_crud():
    client = app.test_client()

    # login to get token
    resp = client.post("/login", json={"username": "testuser", "password": "testpass"})
    token = resp.get_json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create note
    resp = client.post("/notes", json={"title": "Note 1", "content": "content"}, headers=headers)
    assert resp.status_code == 201
    note_id = resp.get_json()["id"]

    # list notes
    resp = client.get("/notes", headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["pagination"]["total"] >= 1

    # update note
    resp = client.patch(f"/notes/{note_id}", json={"title": "Updated"}, headers=headers)
    assert resp.status_code == 200
    assert resp.get_json()["title"] == "Updated"

    # delete note
    resp = client.delete(f"/notes/{note_id}", headers=headers)
    assert resp.status_code == 204