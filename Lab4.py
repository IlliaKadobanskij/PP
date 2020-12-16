from flask import Flask
from itertools import product


student_id = 9
print(list(product(
    ('python 3.8.*', 'python 3.7.*', 'python 3.6.*'),
    ('venv + requirements.txt', 'virtualenv + requirements.txt', 'poetry', 'pipenv')))[student_id - 1])

app = Flask(__name__)


@app.route(f"/api/v1/hello-world-{student_id}")
def hello():
    return f"Hello World {student_id}"


if __name__ == "__main__":
    app.run()
