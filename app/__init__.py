from flask import Flask
from app.main.controllers import main
from app.admin.controllers import admin

app = Flask(__name__)

app.register_blueprint(main, url_prefix="/")
app.register_blueprint(admin, url_prefix="/admin")
