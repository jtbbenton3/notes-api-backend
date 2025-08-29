from peewee import Model, CharField, DateTimeField, SqliteDatabase


database = SqliteDatabase('notes.db')

class BaseModel(Model):
    class Meta:
        database = database

class Note(BaseModel):
    title = CharField(max_length=100)
    content = CharField(max_length=500)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        table_name = 'notes'