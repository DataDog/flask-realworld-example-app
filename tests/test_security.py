from flask import url_for


def test_weak_hash(testapp):
    resp = testapp.get(url_for("security.weak_hash", q="test"))
    assert resp.status_code == 200
    assert len(resp.body) > 0
