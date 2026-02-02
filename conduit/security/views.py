# -*- coding: utf-8 -*-
"""Datadog Security Views
Security views work to validate the below Datadog products in real-world scenarios:
- Application Security Management: [Link](https://docs.datadoghq.com/security/application_security/)
- Application Vulnerability Management (IAST): [Link](https://docs.datadoghq.com/security/application_security/vulnerability_management/)
"""

import json
import os
import random
import re
import subprocess

from flask import Blueprint
from flask import Response
from flask import request
from flask_apispec import use_kwargs
from flask_jwt_extended import jwt_required
from marshmallow import fields
import urllib3

from conduit.articles.models import Article
from conduit.articles.models import Tags
from conduit.articles.serializers import articles_schema
from conduit.security.vulnerabilities import my_function_with_sqli
from conduit.security.vulnerabilities import my_function_with_weak_hash
from conduit.user.models import User


try:
    from ddtrace.appsec._iast._taint_tracking import get_tainted_ranges
    from ddtrace.appsec._iast._taint_tracking import is_pyobject_tainted
except ImportError:
    get_tainted_ranges = lambda x: x  # noqa: E731
    is_pyobject_tainted = lambda x: x  # noqa: E731

blueprint = Blueprint("security", __name__)


def _iast_propagation():
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
    try:
        # SSRF vulnerability
        # requests.get("http://" + string9)
        urllib3.request("GET", "http://" + string9)
    except Exception:
        pass

        # Weak Randomness vulnerability
    _ = random.randint(1, 10)

    # os path propagation
    string14 = os.path.join(string13, "a")  # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted/a
    string15 = os.path.split(string14)[0]  # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted
    string16 = os.path.dirname(
        string15 + "/" + "foobar"
    )  # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted
    string17 = os.path.basename("/foobar/" + string16)  # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted
    string18 = os.path.splitext(string17 + ".jpg")[0]  # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted
    string19 = os.path.normcase(string18)  # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted
    string20 = os.path.splitdrive(string19)[1]  # 1 propagation range: notainted_HIROOT1234-HIROOT123_notainted

    re_slash = re.compile(r"[_.][a-zA-Z]*")
    string21 = re_slash.findall(string20)[0]  # 1 propagation: '_HIROOT

    re_match = re.compile(r"(\w+)", re.IGNORECASE)
    re_match_result = re_match.match(string21)  # 1 propagation: 'HIROOT

    string22 = re_match_result.group(0)  # 1 propagation: '_HIROOT
    # string22 = re_match_result.groups()[0]
    tmp_str = "DDDD"
    string23 = tmp_str + string22  # 1 propagation: 'DDDD_HIROOT

    re_match = re.compile(r"(\w+)(_+)(\w+)", re.IGNORECASE)
    re_match_result = re_match.search(string23)
    string24 = re_match_result.expand(r"DDD_\3")  # 1 propagation: 'DDD_HIROOT

    re_split = re.compile(r"[_.][a-zA-Z]*", re.IGNORECASE)
    re_split_result = re_split.split(string24)

    string25 = re_split_result[0] + " EEE"
    string26 = re.sub(r" EEE", "_OOO", string25, re.IGNORECASE)
    string27 = re.subn(r"OOO", "III", string26, re.IGNORECASE)[0]

    tmp_str2 = "_extend"
    string27 += tmp_str2

    # validates default output and IAST output
    expected = "DDD_III_extend"
    assert string27 == expected, f"Error, string27 is\n{string27}\nExpected:\n{expected}"

    return string27


@blueprint.route("/iast/weak_hash")
def iast_weak_hash():
    data = request.args.get("q")
    return my_function_with_weak_hash(data)


@blueprint.route("/iast/sqli/")
def iast_sqli():
    data = request.args.get("q")
    return my_function_with_sqli(data)


@blueprint.route("/iast/propagation", methods=["GET"])
def iast_propagation():
    """Application Vulnerability Management has 3 key concepts: origins, propagation and sink points (vulnerabilities)
    this view validates some origins, check the propagation of different strings and multiple vulnerabilities
    """

    result = _iast_propagation()
    # Insecure Cookie vulnerability
    resp = Response(
        json.dumps(
            {
                "string_result": result,
                "tainted": is_pyobject_tainted(result),
                "ranges": str(get_tainted_ranges(result)),
            }
        )
    )
    resp.set_cookie("insecure", "cookie", secure=False, httponly=False, samesite="None")
    resp.headers["Vary"] = result
    resp.headers["Header-Injection"] = result

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

    result = _iast_propagation()

    resp.set_cookie("insecure", "cookie", secure=False, httponly=False, samesite="None")
    resp.headers["Vary"] = result
    resp.headers["Header-Injection"] = result

    return resp
