from models import Note, User, database
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def seed_database():
    with database.atomic():
       
        user, created = User.get_or_create(username="testuser", defaults={"password_hash": ""})
        if created or not user.password_hash:
            user.set_password(bcrypt, "testpass")
            user.save()

       
        Note.create(title="First Note", content="This is the first test note.", user=user)
        Note.create(title="Second Note", content="This is the second test note.", user=user)

    print("Database seeded: user 'testuser' with 2 notes.")

if __name__ == "__main__":
    seed_database()