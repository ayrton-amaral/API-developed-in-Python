from flask import Flask
from views.user_view import user
from database.__init__ import database
#pip install flask

app = Flask(__name__)

app.register_blueprint(user)

print("DATABASE CONNECTION -> ", database.dbConnection)

@app.route("/")
def index():
    return "HOME"

if __name__ == "__main__":
    app.run()

#flask --app app run