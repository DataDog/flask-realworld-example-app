# -*- coding: utf-8 -*-
"""Datadog Security Views
Security views work to validate the below Datadog products in real-world scenarios:
- Application Security Management: [Link](https://docs.datadoghq.com/security/application_security/)
- Application Vulnerability Management (IAST): [Link](https://docs.datadoghq.com/security/application_security/vulnerability_management/)
"""
import json
import os
import random
import subprocess

# See comment below on the (disabled) SSRF test
# import requests
# import urllib3
from flask import Blueprint, Response, request

from flask_apispec import use_kwargs
from flask_jwt_extended import jwt_required
from marshmallow import fields
from conduit.articles.models import Article
from conduit.articles.serializers import articles_schema

try:
    from ddtrace.appsec._iast._taint_tracking import get_tainted_ranges
    from ddtrace.appsec._iast._taint_tracking import is_pyobject_tainted
except ImportError:
    get_tainted_ranges = lambda x: x
    is_pyobject_tainted = lambda x: x

blueprint = Blueprint("security", __name__)


@blueprint.route("/iast/propagation", methods=["GET"])
def iast_propagation():
    """Application Vulnerability Management has 3 key concepts: origins, propagation and sink points (vulnerabilities)
    this view validates some origins, check the propagation of different strings and multiple vulnerabilities
    """
    # Origin 1: string1
    origin_string1 = request.args.get("string1")
    # Origin 2: password
    tainted_string_2 = request.args.get("password")

    string1 = str(origin_string1)  # String with 1 propagation range
    string2 = str(tainted_string_2)  # String with 1 propagation range

    string3 = string1 + string2  # 2 propagation ranges: hiroot1234
    string4 = "-".join([string3, string3, string3])  # 6 propagation ranges: hiroot1234-hiroot1234-hiroot1234
    string5 = string4[0:20]  # 1 propagation range: hiroot1234-hiroot123
    string6 = string5.title()  # 1 propagation range: Hiroot1234-Hiroot123
    string7 = string6.upper()  # 1 propagation range: HIROOT1234-HIROOT123
    string8 = "%s_notainted" % string7  # 1 propagation range: HIROOT1234-HIROOT123_notainted
    string9 = "notainted_{}".format(string8)  # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted
    string10 = "nottainted\n" + string9  # 2 propagation ranges: notainted\nnotainted_HIROOT1234-HIROOT123_notainted
    string11 = string10.splitlines()[1]  # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted
    string12 = string11 + "_notainted"  # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted_notainted
    string13 = string12.rsplit("_", 1)[0]  # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted

    try:
        # Path traversal vulnerability
        m = open("/" + string13 + ".txt")
        _ = m.read()
    except Exception:
        pass

    try:
        # Command Injection vulnerability
        _ = subprocess.Popen("ls " + string9)
    except Exception:
        pass

    # Note: this seems to have a leak on ddtrace/contrib/requests/connection.py on the line:
    # with tracer.trace(operation_name, service=service, resource=f"{method} {path}", span_type=SpanTypes.HTTP) as span:
    # Since this hides other potential leaks caused by our aspects, we disabled this test
    # try:
    #     # SSRF vulnerability
    #     # requests.get("http://" + string9)
    #      urllib3.request("GET", "http://" + string9)
    # except Exception:
    #     pass

        # Weak Randomness vulnerability
    _ = random.randint(1, 10)

    # os path propagation
    string14 = os.path.join(string13, "a") # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted/a
    string15 = os.path.split(string14)[0] # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted
    string16 = os.path.dirname(string15 + "/" + "foobar")  # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted
    string17 = os.path.basename("/foobar/" + string16)  # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted
    string18 = os.path.splitext(string17 + ".jpg")[0]  # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted
    string19 = os.path.normcase(string18)  # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted
    string20 = os.path.splitdrive(string19)[1]  # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted

    string20 += "_extend"

    # validates default output and IAST output
    expected = "notainted_HIROOT1234-HIROOT123_notainted_extend"
    assert string20 == expected, f"Error, string 18 is\n{string20}\nExpected:\n{expected}"

    # Insecure Cookie vulnerability
    resp = Response(
        json.dumps(
            {
                "string_result": string20,
                "tainted": is_pyobject_tainted(string20),
                "ranges": str(get_tainted_ranges(string20)),
            }
        )
    )
    resp.set_cookie("insecure", "cookie", secure=False, httponly=False, samesite="None")
    resp.headers["Vary"] = string20
    resp.headers['Header-Injection'] = string20

    return resp


@jwt_required(optional=True)
@use_kwargs(
    {
        "tag": fields.Str(),
        "author": fields.Str(),
        "favorited": fields.Str(),
        "limit": fields.Int(),
        "offset": fields.Int(),
    }
)
@blueprint.route("/iast/articles", methods=["GET"])
def get_articles(tag=None, author=None, favorited=None, limit=20, offset=0):
    # First part, same as /api/articles
    res = Article.query
    if tag:
        res = res.filter(Article.tagList.any(Tags.tagname == tag))
    if author:
        res = res.join(Article.author).join(User).filter(User.username == author)
    if favorited:
        res = res.join(Article.favoriters).filter(User.username == favorited)

    resp = Response(articles_schema.dump(res.offset(offset).limit(limit).all()))

    # Second part, same as method above
    # Origin 1: string1
    origin_string1 = request.args.get("string1")
    # Origin 2: password
    tainted_string_2 = request.args.get("password")

    string1 = str(origin_string1)  # String with 1 propagation range
    string2 = str(tainted_string_2)  # String with 1 propagation range

    string3 = string1 + string2  # 2 propagation ranges: hiroot1234
    string4 = "-".join([string3, string3, string3])  # 6 propagation ranges: hiroot1234-hiroot1234-hiroot1234
    string5 = string4[0:20]  # 1 propagation range: hiroot1234-hiroot123
    string6 = string5.title()  # 1 propagation range: Hiroot1234-Hiroot123
    string7 = string6.upper()  # 1 propagation range: HIROOT1234-HIROOT123
    string8 = "%s_notainted" % string7  # 1 propagation range: HIROOT1234-HIROOT123_notainted
    string9 = "notainted_{}".format(string8)  # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted
    string10 = "nottainted\n" + string9  # 2 propagation ranges: notainted\nnotainted_HIROOT1234-HIROOT123_notainted
    string11 = string10.splitlines()[1]  # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted
    string12 = string11 + "_notainted"  # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted_notainted
    string13 = string12.rsplit("_", 1)[0]  # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted

    try:
        # Path traversal vulnerability
        m = open("/" + string13 + ".txt")
        _ = m.read()
    except Exception:
        pass

    try:
        # Command Injection vulnerability
        _ = subprocess.Popen("ls " + string9)
    except Exception:
        pass

    # Note: this seems to have a leak on ddtrace/contrib/requests/connection.py on the line:
    # with tracer.trace(operation_name, service=service, resource=f"{method} {path}", span_type=SpanTypes.HTTP) as span:
    # Since this hides other potential leaks caused by our aspects, we disabled this test
    # try:
    #     # SSRF vulnerability
    #     # requests.get("http://" + string9)
    #      urllib3.request("GET", "http://" + string9)
    # except Exception:
    #     pass

        # Weak Randomness vulnerability
    _ = random.randint(1, 10)

    # os path propagation
    string14 = os.path.join(string13, "a") # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted/a
    string15 = os.path.split(string14)[0] # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted
    string16 = os.path.dirname(string15 + "/" + "foobar")  # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted
    string17 = os.path.basename("/foobar/" + string16)  # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted
    string18 = os.path.splitext(string17 + ".jpg")[0]  # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted
    string19 = os.path.normcase(string18)  # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted
    string20 = os.path.splitdrive(string19)[1]  # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted

    string20 += "_extend"

    resp.set_cookie("insecure", "cookie", secure=False, httponly=False, samesite="None")
    resp.headers["Vary"] = string20
    resp.headers['Header-Injection'] = string20

    return resp
