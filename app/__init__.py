def create_app(config_name):
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
