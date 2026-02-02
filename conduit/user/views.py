# -*- coding: utf-8 -*-
"""User views."""

from flask import Blueprint
from flask import request
from flask_apispec import marshal_with
from flask_apispec import use_kwargs
from flask_jwt_extended import create_access_token
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

from conduit.database import db
from conduit.exceptions import InvalidUsage
from conduit.profile.models import UserProfile

from .models import User
from .serializers import user_schema


blueprint = Blueprint("user", __name__)


@blueprint.route("/api/users", methods=("POST",))
def register_user(**kwargs):
    data = request.get_json()
    username = data["user"]["username"]
    email = data["user"]["email"]
    password = data["user"]["password"]
    try:
        userprofile = UserProfile(User(username, email, password=password, **kwargs).save()).save()
        userprofile.user.token = create_access_token(identity=userprofile.user)
    except IntegrityError:
        db.session.rollback()
        raise InvalidUsage.user_already_registered()
    return user_schema.dump(userprofile.user)


@blueprint.route("/api/users/login", methods=("POST",))
@jwt_required(optional=True)
def login_user(**kwargs):
    data = request.get_json()
    email = data["user"]["email"]
    password = data["user"]["password"]
    user = User.query.filter_by(email=email).first()
    if user is not None and user.check_password(password):
        user.token = create_access_token(identity=user, fresh=True)
        return user_schema.dump(user)
    else:
        raise InvalidUsage.user_not_found()


@marshal_with(user_schema)
@blueprint.route("/api/user", methods=("GET",))
@jwt_required()
def get_user():
    user = current_user
    # Not sure about this
    user.token = request.headers.environ["HTTP_AUTHORIZATION"].split("Token ")[1]
    return user_schema.dump(user)


@use_kwargs(user_schema)
@marshal_with(user_schema)
@blueprint.route("/api/user", methods=("PUT",))
@jwt_required()
def update_user(**kwargs):
    data = request.get_json()
    email = data["user"]["email"]
    password = data["user"]["password"]
    bio = data["user"]["bio"]
    user = current_user
    if password:
        user.set_password(password)
    if "updated_at" in kwargs:
        kwargs["updated_at"] = user.created_at.replace(tzinfo=None)
    user.update(email=email, bio=bio)
    return user_schema.dump(user)
