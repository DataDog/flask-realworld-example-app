# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

import pytest
from webtest import TestApp

from conduit.app import create_app
from conduit.database import db as _db
from conduit.profile.models import UserProfile
from conduit.settings import TestConfig

from .factories import UserFactory


@pytest.yield_fixture()
def app():
    """An application for the tests."""
    _app = create_app(TestConfig)

    with _app.app_context():
        _db.create_all()

        yield _app


@pytest.fixture(scope="function")
def testapp(app):
    """A Webtest app."""
    return TestApp(app)


@pytest.yield_fixture(scope="function")
def db(app):
    """A database for the tests."""
    _db.app = app
    _db.create_all()
    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture
def user(db):
    """A user for the tests."""

    class User:
        def get(self):
            muser = UserFactory(password="myprecious")
            UserProfile(muser).save()
            db.session.commit()
            return muser

    return User()
