from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from models import database, Note, User

# create app
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "dev-secret-change-this"  # replace before prod

# extensions
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# import routes after extensions so they can use them
from resources import (
    get_notes, create_note, update_note, delete_note,
    signup, login, me
)

# ensure tables exist
with app.app_context():
    database.create_tables([User, Note], safe=True)

# register endpoints
app.add_url_rule('/signup', view_func=signup, methods=['POST'])
app.add_url_rule('/login', view_func=login, methods=['POST'])
app.add_url_rule('/me', view_func=me, methods=['GET'])

app.add_url_rule('/notes', view_func=get_notes, methods=['GET'])
app.add_url_rule('/notes', view_func=create_note, methods=['POST'])
app.add_url_rule('/notes/<int:note_id>', view_func=update_note, methods=['PATCH'])
app.add_url_rule('/notes/<int:note_id>', view_func=delete_note, methods=['DELETE'])

if __name__ == "__main__":
    app.run(debug=True)