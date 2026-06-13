from datetime import datetime

from todo_project import bcrypt, db
from todo_project.models import Task, User, load_user


def test_user_repr(test_app):
    user = User(username="jeff", password="hashed")

    assert repr(user) == "User('jeff')"


def test_task_repr(test_app):
    task = Task(content="Study CI", date_posted=datetime(2024, 1, 1), user_id=1)

    assert repr(task) == "Task('Study CI', '2024-01-01 00:00:00', '1')"


def test_load_user_returns_user(test_app):
    user = User(username="jeff", password="hashed")
    db.session.add(user)
    db.session.commit()

    assert load_user(user.id) == user


def test_password_hash_roundtrip(test_app):
    password = "secret123"
    hashed = bcrypt.generate_password_hash(password).decode("utf-8")

    assert bcrypt.check_password_hash(hashed, password)
