from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route(f"/api/v1/hello-world-<id>")
def hello(id):
    return f"Hello World {id}"


if __name__ == "__main__":
    app.run()
