# SQLAlchemy Foreign Key Relationship Diagram

## Entity-Relationship Diagram (ERD)

```
┌─────────────────────────────┐
│        USER                 │
├─────────────────────────────┤
│ id (PK)                     │
│ username (UNIQUE, NOT NULL) │
│ email (UNIQUE, NULLABLE)    │
└──────────────┬──────────────┘
               │
               │ 1-to-Many
               │ (backref='author')
               │
               ├──────────────────────┐
               │                      │
┌──────────────▼────────────────────────────┐
│        POST                                │
├────────────────────────────────────────────┤
│ id (PK)                                    │
│ title                                      │
│ content                                    │
│ user_id (FK → user.id, NOT NULL) ◀────────┤ Foreign Key Reference
└────────────────────────────────────────────┘
```

---

## Table Structure

### USER Table
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    email VARCHAR UNIQUE
);
```

### POSTS Table
```sql
CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    title VARCHAR,
    content TEXT,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id)
);
```

---

## SQLAlchemy Model Definition

```python
# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True)
    posts = db.relationship('Post', backref='author', lazy=True)

# Post Model
class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
```

---

## How Foreign Key Works

### 1. Creating a User
```python
user = User(username="alice", email="alice@example.com")
db.session.add(user)
db.session.commit()
# User ID = 1
```

### 2. Creating a Post (with FK reference)
```python
post = Post(title="My Post", content="Content here", user_id=user.id)
db.session.add(post)
db.session.commit()
# Post.user_id = 1 (references user.id)
```

### 3. Accessing Related Data (FK in Action)

**From User to Posts (1-to-Many):**
```python
user = User.query.get(1)
for post in user.posts:
    print(post.title)  # Prints all posts by this user
```

**From Post to User (Many-to-One):**
```python
post = Post.query.get(1)
print(post.author.username)  # Prints "alice"
print(post.author.email)     # Prints "alice@example.com"
```

---

## Constraint Enforcement

### Valid Operation ✓
```python
# User exists with id=1
user = User.query.get(1)

# Create post with valid FK
post = Post(title="Post", content="Content", user_id=1)
db.session.add(post)
db.session.commit()  # ✓ SUCCESS
```

### Invalid Operation ✗
```python
# Create post with non-existent user
post = Post(title="Post", content="Content", user_id=999)
db.session.add(post)
db.session.commit()  # ✗ FAILS - FK constraint violation
```

---

## Relationship Metadata

```
┌────────────────────────────────────────┐
│ User ←→ Post Relationship Metadata     │
├────────────────────────────────────────┤
│ Type: One-to-Many                      │
│ Foreign Key: posts.user_id → user.id  │
│ Lazy Loading: True (load on access)   │
│ Backref: 'author'                      │
│ ├─ Access from Post: post.author       │
│ └─ Access from User: user.posts        │
│ Cascade: None (default)                │
└────────────────────────────────────────┘
```

---

## Sample Data Relationships

```
User "Aziz" (ID=1)
    │
    ├─ Post: "First Post" (user_id=1)
    ├─ Post: "Second Post" (user_id=1)
    └─ Post: "Another Post" (user_id=1)

User "Fatima" (ID=2)
    │
    └─ Post: "Hello World" (user_id=2)

User "Mohammed" (ID=3)
    │
    └─ Post: "Learning SQLAlchemy" (user_id=3)
```

---

## Foreign Key Verification Matrix

| Post ID | Post Title | user_id | User ID | Username | Status |
|---------|-----------|---------|---------|----------|--------|
| 1 | First Post | 1 | 1 | Aziz | ✓ Valid |
| 2 | Hello World | 2 | 2 | Fatima | ✓ Valid |
| 3 | Learning SQLAlchemy | 3 | 3 | Mohammed | ✓ Valid |
| 4 | Second Post | 1 | 1 | Aziz | ✓ Valid |

---

## API Endpoints Using Foreign Keys

### 1. GET /users
Returns all users (no FK needed)
```json
[
  {"id": 1, "username": "alice", "email": "alice@example.com"},
  {"id": 2, "username": "bob", "email": "bob@example.com"}
]
```

### 2. POST /users
Create user (no FK needed)
```json
{
  "username": "new_user",
  "email": "new@example.com"
}
```

### 3. GET /posts
Returns all posts WITH author info (uses FK relationship)
```json
[
  {
    "id": 1,
    "title": "First Post",
    "content": "Content...",
    "user_id": 1,
    "username": "alice"  ← FROM FK RELATIONSHIP
  }
]
```

### 4. POST /posts
Create post (REQUIRES valid FK)
```json
{
  "title": "New Post",
  "content": "Content...",
  "user_id": 1  ← MUST REFERENCE EXISTING USER
}
```
Response if FK invalid:
```json
{"message": "User not found"} → 400 Error
```

### 5. GET /verify
Shows complete FK relationship structure
```json
{
  "users_count": 3,
  "posts_count": 4,
  "users": [
    {
      "id": 1,
      "username": "alice",
      "posts": [
        {"id": 1, "title": "First Post"},
        {"id": 4, "title": "Second Post"}
      ]
    }
  ],
  "posts": [
    {
      "id": 1,
      "title": "First Post",
      "user_id": 1,
      "author": {"id": 1, "username": "alice"}
    }
  ]
}
```

---

## Key Takeaways

✓ **Foreign Key Defined**: Post.user_id references User.id
✓ **NOT NULL Constraint**: Posts cannot exist without a user
✓ **Bidirectional Access**: Navigate from User to Posts and vice versa
✓ **Validation**: Routes validate FK exists before creating posts
✓ **Referential Integrity**: Database maintains relationship consistency
✓ **Sample Data**: Pre-populated with valid FK relationships

