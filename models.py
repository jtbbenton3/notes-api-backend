from peewee import Model, CharField, TextField, DateTimeField
from playhouse.db_url import connect

# Database connection
database = connect('sqlite:///notes.db')

class BaseModel(Model):
    class Meta:
        database = database

class Note(BaseModel):
    title = CharField(max_length=100)
    content = TextField()
    created_at = DateTimeField(default=None)  
    updated_at = DateTimeField(default=None)  

    def save(self, *args, **kwargs):
        from datetime import datetime
        if not self.created_at:
            self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        return super(Note, self).save(*args, **kwargs)

# Create tables
with database:
    database.create_tables([Note], safe=True)