from models import Note, database

def seed_data():
    with database.atomic():
        # Clear existing notes
        Note.delete().execute()
        # Add sample notes
        Note.create(title="First Note", content="This is the first test note.")
        Note.create(title="Second Note", content="This is the second test note.")
        print("Database seeded with 2 sample notes.")

if __name__ == "__main__":
    seed_data()