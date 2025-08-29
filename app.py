from flask import Flask
from models import database, Note  

app = Flask(__name__)

# Initialize the database
with app.app_context():
    database.create_tables([Note], safe=True)

if __name__ == "__main__":
    app.run(debug=True)