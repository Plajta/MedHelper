if __name__ == "__main__":
    from src.backend import db, create_app, models
    db.create_all(app=create_app())