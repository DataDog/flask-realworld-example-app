# coding: utf-8

from flask import Blueprint
from flask_apispec import marshal_with
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required

from conduit.exceptions import InvalidUsage
from conduit.user.models import User

from .serializers import profile_schema


blueprint = Blueprint("profiles", __name__)


@marshal_with(profile_schema)
@blueprint.route("/api/profiles/<username>", methods=("GET",))
@jwt_required(optional=True)
def get_profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        raise InvalidUsage.user_not_found()
    return profile_schema.dump(user.profile)


@marshal_with(profile_schema)
@blueprint.route("/api/profiles/<username>/follow", methods=("POST",))
@jwt_required()
def follow_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        raise InvalidUsage.user_not_found()
    current_user.profile.follow(user.profile)
    current_user.profile.save()
    return profile_schema.dump(user.profile)


@marshal_with(profile_schema)
@blueprint.route("/api/profiles/<username>/follow", methods=("DELETE",))
@jwt_required()
def unfollow_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        raise InvalidUsage.user_not_found()
    current_user.profile.unfollow(user.profile)
    current_user.profile.save()
    return profile_schema.dump(user.profile)
