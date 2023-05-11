from place_remember import create_app, db
from place_remember.authorization import init_config

if __name__ == "__main__":
    app = create_app()
    init_config(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
