from app import app

if __name__ == "__main__":
    app.run(host=app.config["FLASK_HOST"], port=app.config["FLASK_PORT"], debug=app.config["FLASK_DEBUG"])