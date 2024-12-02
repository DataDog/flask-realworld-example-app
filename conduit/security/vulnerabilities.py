import hashlib


def my_function_with_weak_hash(data):
    return hashlib.md5(data).hexdigest()
