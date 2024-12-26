
# Python DAO and DTO Example

This repository demonstrates how to implement **Data Access Object (DAO)** and **Data Transfer Object (DTO)** patterns in Python. The example is based on a simple `User` management system using SQLite.

---

## Getting Started

### Prerequisites
- Python 3.7 or above
- SQLite (comes pre-installed with Python)

---

## Code Overview

### Data Transfer Object (DTO)

The `UserDTO` class is a lightweight object used to transfer data between layers.

```python
class UserDTO:
    def __init__(self, user_id: int, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email

    def __repr__(self):
        return f"UserDTO(user_id={self.user_id}, name='{self.name}', email='{self.email}')"
```

###Data Access Object (DAO)

The UserDAO class manages the interactions with the database. It supports operations like CRUD (Create, Read, Update, Delete).

```python
import sqlite3
from typing import List, Optional

class UserDAO:
    def __init__(self, db_path: str = ":memory:"):
        self.connection = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL
                )
            """)

    def add_user(self, user: UserDTO) -> int:
        with self.connection:
            cursor = self.connection.execute(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                (user.name, user.email)
            )
            return cursor.lastrowid

    def get_user(self, user_id: int) -> Optional[UserDTO]:
        cursor = self.connection.execute(
            "SELECT user_id, name, email FROM users WHERE user_id = ?",
            (user_id,)
        )
        row = cursor.fetchone()
        if row:
            return UserDTO(*row)
        return None

    def get_all_users(self) -> List[UserDTO]:
        cursor = self.connection.execute(
            "SELECT user_id, name, email FROM users"
        )
        rows = cursor.fetchall()
        return [UserDTO(*row) for row in rows]

    def update_user(self, user: UserDTO) -> bool:
        with self.connection:
            result = self.connection.execute(
                "UPDATE users SET name = ?, email = ? WHERE user_id = ?",
                (user.name, user.email, user.user_id)
            )
            return result.rowcount > 0

    def delete_user(self, user_id: int) -> bool:
        with self.connection:
            result = self.connection.execute(
                "DELETE FROM users WHERE user_id = ?",
                (user_id,)
            )
            return result.rowcount > 0
```

##Example Usage

### Example usage
```python
if __name__ == "__main__":
    dao = UserDAO()

    # Add a user
    user_id = dao.add_user(UserDTO(None, "Alice", "alice@example.com"))
    print(f"User added with ID: {user_id}")

    # Retrieve user
    user = dao.get_user(user_id)
    print(f"Retrieved: {user}")

    # Update user
    user.name = "Alice Smith"
    dao.update_user(user)
    print(f"Updated user: {dao.get_user(user_id)}")

    # List all users
    print("All users:", dao.get_all_users())

    # Delete user
    dao.delete_user(user_id)
    print("All users after deletion:", dao.get_all_users())
```
##Features
	•	Lightweight DTO for data transfer
	•	DAO implementation for database interactions
	•	Basic CRUD operations (Create, Read, Update, Delete)
	•	Uses SQLite for simplicity

Directory Structure

.
├── main.py        # Entry point with usage examples
├── dao.py         # DAO implementation
├── dto.py         # DTO implementation
└── README.md      # Documentation
