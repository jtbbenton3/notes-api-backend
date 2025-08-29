from marshmallow import Schema, fields, ValidationError

class NoteSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, max_length=100)
    content = fields.Str(required=True, max_length=500)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @staticmethod
    def validate_note(data):
        schema = NoteSchema()
        try:
            return schema.load(data)
        except ValidationError as err:
            raise ValidationError(err.messages)

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)