from flask import url_for


def test_weak_hash(testapp):
    resp = testapp.get(url_for("security.iast_weak_hash", q="test"))
    assert resp.status_code == 200
    assert len(resp.body) > 0


def test_sqli(testapp):
    resp = testapp.get(url_for("security.iast_sqli", q="test"))
    assert resp.status_code == 200
    assert resp.body == b""
