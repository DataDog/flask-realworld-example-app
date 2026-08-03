# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""

from flask import Flask

from conduit import articles
from conduit import commands
from conduit import profile
from conduit import security
from conduit import user
from conduit.exceptions import InvalidUsage
from conduit.extensions import bcrypt
from conduit.extensions import cache
from conduit.extensions import db
from conduit.extensions import jwt
from conduit.extensions import migrate
from conduit.settings import ProdConfig


def create_app(config_object=ProdConfig):
    """An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(profile.views.blueprint)
    app.register_blueprint(articles.views.blueprint)
    app.register_blueprint(security.views.blueprint)

    # Optional: register a basic health endpoint and Prometheus metrics
    # if the helper modules are available at runtime. We import inside
    # the function to avoid forcing extra dependencies during install.
    try:
        from app_health import health_bp

        app.register_blueprint(health_bp)
    except Exception:
        # If the module isn't present or registration fails, continue silently.
        pass

    try:
        from metrics import after_request, metrics_endpoint

        # Register a simple after_request hook to collect request metrics
        app.after_request(after_request)
        # Expose Prometheus metrics at /metrics
        app.add_url_rule("/metrics", "metrics", metrics_endpoint)
    except Exception:
        pass


def register_errorhandlers(app):
    def errorhandler(error):
        response = error.to_json()
        response.status_code = error.status_code
        return response

    app.errorhandler(InvalidUsage)(errorhandler)


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {
            "db": db,
            "User": user.models.User,
            "UserProfile": profile.models.UserProfile,
            "Article": articles.models.Article,
            "Tag": articles.models.Tags,
            "Comment": articles.models.Comment,
        }

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
