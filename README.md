# Notes API Backend

## Project Summary
I’m building a Flask API with JWT authentication for a Notes app. Users can register, log in, and manage their own notes with CRUD operations. The GET /notes endpoint will have pagination, and all endpoints will be protected to ensure only the owner can access their notes.

## Design Plan
### Models
- `User`: `id` (primary key), `username` (unique, String), `password_hash` (String, Bcrypt).
- `Notes`: `id` (primary key), `title` (String, non-empty), `content` (Text), `user_id` (foreign key to `User`).

### Relationships
- `User` has many `Notes`.
- `Notes` belongs to `User`.

### Endpoints
- **Auth**: 
  - `POST /signup`
  - `POST /login`
  - `GET /me`
- **Notes**: 
  - `GET /notes` (paginated)
  - `POST /notes`
  - `PATCH /notes/<id>`
  - `DELETE /notes/<id>`

### Schemas
- `UserSchema`: fields `id`, `username` (validate unique `username`).
- `NoteSchema`: fields `id`, `title`, `content`, `user_id` (validate non-empty `title`).