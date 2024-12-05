import hashlib

from sqlalchemy import text

from conduit.database import db


def my_function_with_weak_hash(data):
    return hashlib.md5(data.encode()).hexdigest()


def my_function_with_sqli(data):
    q = "SELECT * FROM users WHERE username != '" + data + "'"
    query = text(q)
    res = db.session.execute(query)
    return ", ".join(res.fetchall())
