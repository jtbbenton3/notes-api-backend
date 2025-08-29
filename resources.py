from flask import request, jsonify
from models import Note, database

# Create new note
def create_note():
    data = request.get_json()
    with database.atomic():
        note = Note.create(title=data['title'], content=data['content'])
    return jsonify({"id": note.id, "title": note.title, "content": note.content}), 201

# notes
def get_notes():
    notes = Note.select()
    return jsonify([{"id": note.id, "title": note.title, "content": note.content, "created_at": note.created_at.isoformat()} for note in notes]), 200