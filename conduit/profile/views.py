# coding: utf-8

from flask import Blueprint
from flask_apispec import marshal_with
from flask_jwt_extended import current_user, jwt_required

from conduit.exceptions import InvalidUsage
from conduit.user.models import User
from .serializers import profile_schema

blueprint = Blueprint("profiles", __name__)


@jwt_required(optional=True)
@marshal_with(profile_schema)
@blueprint.route("/api/profiles/<username>", methods=("GET",))
def get_profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        raise InvalidUsage.user_not_found()
    return user.profile


@jwt_required
@marshal_with(profile_schema)
@blueprint.route("/api/profiles/<username>/follow", methods=("POST",))
def follow_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        raise InvalidUsage.user_not_found()
    current_user.profile.follow(user.profile)
    current_user.profile.save()
    return user.profile


@jwt_required
@marshal_with(profile_schema)
@blueprint.route("/api/profiles/<username>/follow", methods=("DELETE",))
def unfollow_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        raise InvalidUsage.user_not_found()
    current_user.profile.unfollow(user.profile)
    current_user.profile.save()
    return user.profile
