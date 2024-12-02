# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""

def jwt_identity(*args, **kwargs):
    from conduit.user.models import User
    return User.get_by_id(args[1]["sub"])


def identity_loader(*args, **kwargs):
    return args[0].id
