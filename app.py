"""
GuestSphere - Smart Guest Management & Event Attendance Tracking System
Entry point: run with `python app.py`
"""
import os
from flask import Flask, render_template
from flask_login import LoginManager
from config import Config
from models import db, User


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure runtime folders exist
    for folder in [app.config["UPLOAD_FOLDER"], app.config["FACE_DATA_FOLDER"], app.config["MODELS_DATA_FOLDER"]]:
        os.makedirs(folder, exist_ok=True)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "warning"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.events import events_bp
    from routes.guests import guests_bp
    from routes.invitations import invitations_bp
    from routes.rsvp import rsvp_bp
    from routes.attendance import attendance_bp
    from routes.qr_checkin import qr_checkin_bp
    from routes.face_recognition import face_bp
    from routes.seating import seating_bp
    from routes.reports import reports_bp
    from routes.notifications import notifications_bp
    from routes.settings import settings_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(guests_bp)
    app.register_blueprint(invitations_bp)
    app.register_blueprint(rsvp_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(qr_checkin_bp)
    app.register_blueprint(face_bp)
    app.register_blueprint(seating_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(settings_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403

    @app.errorhandler(500)
    def server_error(e):
        return render_template("errors/500.html"), 500

    # Make current app name available in all templates
    @app.context_processor
    def inject_globals():
        from models import Notification
        unread_count = 0
        try:
            unread_count = Notification.query.filter_by(is_read=False).count()
        except Exception:
            pass
        return {"app_name": app.config["APP_NAME"], "unread_notifications": unread_count}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
