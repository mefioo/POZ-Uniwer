from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '3d6f45a5fc12445dbac2f59c3b6c7cb1'

from app import routes