from flask import request, jsonify
from models import Note, database
from schemas import note_schema, NoteSchema
from marshmallow import ValidationError

# Create a new note
def create_note():
    data = request.get_json()
    try:
        validated_data = NoteSchema().load(data)  
        with database.atomic():
            note = Note.create(title=validated_data['title'], content=validated_data['content'])
        return note_schema.dump(note), 201
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

# List all notes
def get_notes():
    notes = Note.select()
    return NoteSchema(many=True).dump(notes), 200  