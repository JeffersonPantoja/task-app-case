from types import SimpleNamespace

from todo_project import bcrypt, db
from todo_project.forms import RegistrationForm, UpdateUserInfoForm
from todo_project.models import User


def test_registration_form_accepts_new_username(test_app):
    with test_app.test_request_context(
        method="POST",
        data={
            "username": "jefferson",
            "password": "secret123",
            "confirm_password": "secret123",
        },
    ):
        form = RegistrationForm()

        assert form.validate() is True


def test_registration_form_rejects_existing_username(test_app):
    user = User(username="jefferson", password=bcrypt.generate_password_hash("secret123").decode("utf-8"))
    db.session.add(user)
    db.session.commit()

    with test_app.test_request_context(
        method="POST",
        data={
            "username": "jefferson",
            "password": "secret123",
            "confirm_password": "secret123",
        },
    ):
        form = RegistrationForm()

        assert form.validate() is False
        assert "Username Exists" in form.username.errors


def test_update_user_info_form_allows_current_username(test_app, monkeypatch):
    monkeypatch.setattr("todo_project.forms.current_user", SimpleNamespace(username="jefferson"))

    with test_app.test_request_context(
        method="POST",
        data={"username": "jefferson"},
    ):
        form = UpdateUserInfoForm()

        assert form.validate() is True
