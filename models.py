from peewee import Model, CharField, TextField, DateTimeField, ForeignKeyField
from playhouse.db_url import connect

# DB: sqlite file in project root
database = connect('sqlite:///notes.db')

class BaseModel(Model):
    class Meta:
        database = database

class User(BaseModel):
    username = CharField(unique=True)
    # store ONLY the hash
    password_hash = CharField()

    class Meta:
        table_name = 'users'

    # helpers (no app context required)
    def set_password(self, bcrypt, raw_password: str):
        self.password_hash = bcrypt.generate_password_hash(raw_password).decode("utf-8")

    def check_password(self, bcrypt, raw_password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, raw_password)

class Note(BaseModel):
    title = CharField(max_length=100)
    content = TextField()
    created_at = DateTimeField(null=True)
    updated_at = DateTimeField(null=True)
    user = ForeignKeyField(User, backref='notes')

    def save(self, *args, **kwargs):
        from datetime import datetime
        if not self.created_at:
            self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        return super(Note, self).save(*args, **kwargs)

# Create tables if missing
with database:
    database.create_tables([User, Note], safe=True)