"""
start application
"""
from flask import Flask
import flask_sqlalchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Fsmnl2002@localhost/delivery_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = flask_sqlalchemy.SQLAlchemy(app)


@app.route('/')
def index():
    """
    main page
    """
    return "Hello world"


if __name__ == "__main__":
    app.run(debug=True)
