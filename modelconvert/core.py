# -*- coding: utf-8 -*-

from flask import Flask

from .extensions import celery
from .frontend import frontend


# -- App setup --------------------------------------------------------------
def create_app():
    """Create the Flask app."""

    app = Flask("modelconvert")
    app.config.from_object('modelconvert.settings')
    app.config.from_envvar('MODELCONVERT_SETTINGS', silent=True)

    celery.add_defaults(app.config)

    app.register_blueprint(frontend)

    # configure error handlers
    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template("403.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("500.html"), 500

    return app



if __name__ == "__main__":
    app.run()
