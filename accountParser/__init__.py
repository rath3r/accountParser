import os
from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    app.config.from_prefixed_env()
    try:
        devDB = app.config["DEV_DB"]
        print("Using DEV DB")
    except:
        devDB = False
        print("Using PROD DB")
    
    if devDB is True:
        app.config.from_mapping(
            DATABASE=os.path.join(app.instance_path, 'accountParserDev.sqlite'),
        )
    else:
        app.config.from_mapping(
            DATABASE=os.path.join(app.instance_path, 'accountParser.sqlite'),
        )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import process, home, categories, entries
    app.register_blueprint(home.bp)
    app.register_blueprint(process.bp)
    app.register_blueprint(categories.bp)
    app.register_blueprint(entries.bp)
    
    return app