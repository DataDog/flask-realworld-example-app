# -*- coding: utf-8 -*-
"""Create an application instance."""

from flask.helpers import get_debug_flag

from conduit.app import create_app
from conduit.settings import DevConfig
from conduit.settings import ProdConfig


CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = create_app(CONFIG)


@app.route("/")
@app.route("/index")
def index():
    return "HELLO"


if __name__ == "__main__":
    app.run(debug=True, port=8000)
