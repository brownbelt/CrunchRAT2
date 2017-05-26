from app.main.views import main
from app.admin.views import admin
from flask import Flask

app = Flask(__name__)

app.register_blueprint(main, url_prefix="/")
app.register_blueprint(admin, url_prefix="/admin")
