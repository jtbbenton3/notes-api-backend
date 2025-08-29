from flask import Flask
from models import database, Note
from resources import create_note, get_notes

app = Flask(__name__)

# Initialize the database
with app.app_context():
    database.create_tables([Note], safe=True)

# Register endpoints
app.route('/notes', methods=['GET'])(get_notes)
app.route('/notes', methods=['POST'])(create_note)

if __name__ == "__main__":
    app.run(debug=True)