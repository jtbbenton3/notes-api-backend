from flask import request, jsonify
from models import Note, User, database
from schemas import note_schema, NoteSchema
from marshmallow import ValidationError

# Create a new note
def create_note():
    data = request.get_json()
    try:
        validated_data = NoteSchema().load(data)  
        with database.atomic():
            user = User.get_or_none(username="testuser")
            if not user:
                return jsonify({"error": "User not found"}), 404
            note = Note.create(title=validated_data['title'], content=validated_data['content'], user=user)
        return note_schema.dump(note), 201
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

# List all notes
def get_notes():
    notes = Note.select().where(Note.user == User.get(username="testuser"))
    return NoteSchema(many=True).dump(notes), 200