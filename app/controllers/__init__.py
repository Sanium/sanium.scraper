from . import JobController


def init_app(app):
    app.register_blueprint(JobController.bp)
