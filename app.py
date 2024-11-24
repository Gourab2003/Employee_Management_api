from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate =  Migrate()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:gourab@localhost/employee_mgmt'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from routes import employee_bp
    app.register_blueprint(employee_bp, url_prefix='/api')
    
    return app