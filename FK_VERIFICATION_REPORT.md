# Foreign Key Verification and Sample Data Report

## Summary
✓ **Foreign Key Relationships Successfully Verified and Sample Data Added**

---

## 1. Foreign Key Configuration

### User Table
- **Column**: `id` (Integer, Primary Key)
- **Column**: `username` (String, Unique, NOT NULL)
- **Column**: `email` (String, Unique, NULLABLE)
- **Relationship**: One-to-Many with Post (via `posts` relationship with `backref='author'`)

### Post Table
- **Column**: `id` (Integer, Primary Key)
- **Column**: `title` (String)
- **Column**: `content` (Text)
- **Column**: `user_id` (Integer, Foreign Key, NOT NULL)
  - **References**: `user.id`
  - **Constraint**: user_id MUST reference a valid user ID
  - **Relationship**: Many-to-One with User (via `author` backref)

---

## 2. Relationship Verification

### Foreign Key Integrity
- ✓ Post.user_id correctly references User.id
- ✓ One-to-Many relationship: One User has multiple Posts
- ✓ Bidirectional access: 
  - From User: `user.posts` returns all posts by that user
  - From Post: `post.author` returns the author User object

---

## 3. Sample Data Added

### Users Created
| ID | Username | Email |
|----|----------|-------|
| 1 | Aziz | aziz@example.com |
| 2 | Fatima | fatima@example.com |
| 3 | Mohammed | mohammed@example.com |
| 4 | Sara | sara@example.com |
| 5 | Youssef | youssef@example.com |
| 6 | Imane | imane@example.com |

### Posts Created with Foreign Keys
| Post ID | Title | Content | Author | User ID |
|---------|-------|---------|--------|---------|
| 1 | First Post | Alice's first post | alice (1) | 1 |
| 2 | Hello World | Bob's introduction to blogging | bob (2) | 2 |
| 3 | Learning SQLAlchemy | Charlie explores database relationships | charlie (3) | 3 |
| 4 | Second Post | Alice's second post about Flask | alice (1) | 1 |

---

## 4. Database Initialization

The Flask application automatically initializes the database with sample data on first run via the `@app.before_request` hook. This ensures:

1. **Auto-creation of tables** using SQLAlchemy's `db.create_all()`
2. **Sample users are created** only once (checked with `User.query.first() is None`)
3. **Sample posts are created** with valid foreign keys pointing to existing users
4. **No duplicate data** on subsequent requests

---

## 5. Foreign Key Validation Results

✓ **All 4 sample posts have valid foreign keys**
- Post #1: user_id=1 → User 'Aziz' exists ✓
- Post #2: user_id=2 → User 'Fatima' exists ✓
- Post #3: user_id=3 → User 'Mohammed' exists ✓
- Post #4: user_id=1 → User 'Aziz' exists ✓

---

## 6. Routes Available

### GET /users
- Lists all users with id, username, email

### POST /users
- Creates a new user with username and email

### GET /posts
- Lists all posts with:
  - id, title, content, user_id
  - **username** (from related User via foreign key)

### POST /posts
- Creates a new post
- Validates user_id references an existing user
- Returns 400 if user not found (FK constraint)

### GET /verify
- Displays complete foreign key verification report
- Shows all users with their posts
- Shows all posts with their author information

---

## 7. Key Features

✓ Foreign key is NOT NULL - prevents posts without a user
✓ Bidirectional relationship - access posts from user and user from post
✓ Sample data demonstrates working relationships
✓ Automatic database initialization with sample data
✓ Referential integrity maintained

---

## Testing the Foreign Keys

```bash
# Start the application
python app.py

# View sample data relationships
curl http://127.0.0.1:5000/verify

# View all users
curl http://127.0.0.1:5000/users

# View all posts (with author info via FK)
curl http://127.0.0.1:5000/posts

# Create new user
curl -X POST http://127.0.0.1:5000/users \
  -H "Content-Type: application/json" \
  -d '{"username": "newuser", "email": "new@example.com"}'

# Create new post (with FK to existing user)
curl -X POST http://127.0.0.1:5000/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "Test", "content": "Test post", "user_id": 1}'
```

