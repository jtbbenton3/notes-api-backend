from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from flask_bcrypt import Bcrypt
from models import database, User, Note
from schemas import note_schema, notes_schema, user_schema
from math import ceil


bcrypt = Bcrypt()



def signup():
    data = request.get_json() or {}
    errors = user_schema.validate(data, partial=("id",))
    if errors:
        return jsonify({"errors": errors}), 422

    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 422

    if User.select().where(User.username == username).exists():
        return jsonify({"error": "username already taken"}), 422

    with database.atomic():
        user = User(username=username, password_hash="")
        user.set_password(bcrypt, password)
        user.save()

    return jsonify({"id": user.id, "username": user.username}), 201


def login():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    user = User.get_or_none(User.username == username)
    if not user or not user.check_password(bcrypt, password):
        return jsonify({"error": "invalid credentials"}), 401

    token = create_access_token(identity=user.id)
    return jsonify({"access_token": token}), 200


@jwt_required()
def me():
    uid = get_jwt_identity()
    user = User.get_by_id(uid)
    return jsonify({"id": user.id, "username": user.username}), 200




@jwt_required()
def create_note():
    data = request.get_json() or {}
    errors = note_schema.validate(data, partial=("id", "created_at", "updated_at", "user_id"))
    if errors:
        return jsonify({"errors": errors}), 422

    uid = get_jwt_identity()
    user = User.get_by_id(uid)

    with database.atomic():
        note = Note.create(
            title=data["title"].strip(),
            content=data["content"],
            user=user
        )
    return note_schema.dump(note), 201


@jwt_required()
def get_notes():
    uid = get_jwt_identity()
    user = User.get_by_id(uid)

    
    try:
        page = max(1, int(request.args.get("page", 1)))
    except ValueError:
        page = 1
    try:
        per_page = int(request.args.get("per_page", 10))
    except ValueError:
        per_page = 10
    per_page = max(1, min(50, per_page))

    query = Note.select().where(Note.user == user).order_by(Note.created_at.desc())
    total = query.count()
    pages = max(1, ceil(total / per_page)) if total else 1
    items = list(query.paginate(page, per_page))

    return jsonify({
        "items": notes_schema.dump(items),
        "pagination": {"page": page, "per_page": per_page, "total": total, "pages": pages}
    }), 200


@jwt_required()
def update_note(note_id: int):
    uid = get_jwt_identity()
    user = User.get_by_id(uid)

    note = Note.get_or_none(Note.id == note_id, Note.user == user)
    if not note:
        return jsonify({"error": "not found"}), 404

    data = request.get_json() or {}
    
    title = data.get("title")
    content = data.get("content")

    if title is not None:
        if not str(title).strip():
            return jsonify({"error": "title cannot be empty"}), 422
        note.title = str(title).strip()
    if content is not None:
        note.content = content

    with database.atomic():
        note.save()

    return note_schema.dump(note), 200


@jwt_required()
def delete_note(note_id: int):
    uid = get_jwt_identity()
    user = User.get_by_id(uid)

    note = Note.get_or_none(Note.id == note_id, Note.user == user)
    if not note:
        return jsonify({"error": "not found"}), 404

    with database.atomic():
        note.delete_instance()

    return '', 204