from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_dump
from marshmallow import pre_load


class ProfileSchema(Schema):
    username = fields.Str()
    email = fields.Email()
    password = fields.Str(load_only=True)
    bio = fields.Str()
    image = fields.Url()
    following = fields.Boolean()
    # ugly hack.
    profile = fields.Nested("self", exclude=("profile",), default=True, load_only=True)

    @pre_load
    def make_user(self, data, **kwargs):
        return data["profile"]

    @post_dump
    def dump_user(self, data, **kwargs):
        return {"profile": data}

    class Meta:
        strict = True


profile_schema = ProfileSchema()
profile_schemas = ProfileSchema(many=True)
