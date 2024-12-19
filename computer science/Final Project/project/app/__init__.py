from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config
from flask_wtf import CSRFProtect
#from app.models import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from flask_socketio import SocketIO
#def create_app():

# Create Flask application
app = Flask(__name__)

# Enable CORS to allow requests from different origins
CORS(app)

# Load configuration from Config object
app.config.from_object(Config)

# Initialize SocketIO to handle WebSockets
socketio = SocketIO(app)

# Initialize SQLAlchemy to handle the database
db = SQLAlchemy()
db.init_app(app)

# Initialize Flask-Migrate to handle database migrations
migrate = Migrate(app, db)

# Initialize the user session manager
login_manager = LoginManager(app)
login_manager.login_view = 'user.login'

# Protect against CSRF attacks
csrf = CSRFProtect(app)

# Import Blueprints to manage different routes
from app.routes import user_bp
from app.routes import event_bp
from app.routes import ocurrence_bp
from app.routes import comment_bp

# Register Blueprints in the app
app.register_blueprint(user_bp)
app.register_blueprint(event_bp)
app.register_blueprint(ocurrence_bp)
app.register_blueprint(comment_bp)

# Load the user from the database
@login_manager.user_loader
def load_user(user_id):
    from app.models import User  # Importar aquí para evitar circular imports
    return User.query.get(int(user_id))


#from models import User, Role, Event, EventType, EventOccurrence, SurveyOption, SurveyResponse, Comment

# Application context to initialize the database
with app.app_context():
    db.create_all()

    #Import Category model, If there is no category, create some by default
    from app.models import Category
    if not Category.query.first():
        category = Category(name='general')
        db.session.add(category)

        category = Category(name='football')
        db.session.add(category)

        db.session.commit()

    #Import Role model, If there is no role, create some by default
    from app.models import Role
    if not Role.query.first():
        viewer_role = Role(name='viewer')
        db.session.add(viewer_role)

        journalist_role = Role(name='journalist')
        db.session.add(journalist_role)

        administrator_role = Role(name='administrator')
        db.session.add(administrator_role)

        db.session.commit()

    #Import User model, If there is no user, create admin user
    from app.models import User
    if not User.query.first():
        admin_role = Role.query.filter(Role.name=="administrator").first()
        admin = User(
                name='admin',
                email='admin@mail.com',
                password=generate_password_hash('admin'),  # Asegúrate de hashear la contraseña
                id_role=admin_role.id  # Asigna un rol, asegúrate de que este ID exista en la tabla roles
            )
        db.session.add(admin)

    db.session.commit()



#flask db init
#flask db migrate -m "Initial migration."
#flask db upgrade
