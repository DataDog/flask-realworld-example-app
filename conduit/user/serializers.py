# coding: utf-8

from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_dump
from marshmallow import pre_load


class UserSchema(Schema):
    username = fields.Str()
    email = fields.Email()
    password = fields.Str(load_only=True)
    bio = fields.Str()
    image = fields.Url()
    token = fields.Str(dump_only=True)
    createdAt = fields.DateTime(attribute="created_at", dump_only=True)
    updatedAt = fields.DateTime(attribute="updated_at")
    # ugly hack.
    user = fields.Nested("self", exclude=("user",), default=True, load_only=True)

    @pre_load
    def make_user(self, data, **kwargs):
        user_data = data["user"]
        # some of the frontends send this like an empty string and some send
        # null
        if not user_data.get("email", True):
            del user_data["email"]
        if not user_data.get("image", True):
            del user_data["image"]
        return user_data

    @post_dump
    def dump_user(self, data, **kwargs):
        return {"user": data}

    class Meta:
        fields = ("username", "email", "password", "bio", "token")


user_schema = UserSchema()
user_schemas = UserSchema(many=True)
