from flask import Flask
from flask import render_template
from flask import request
from app.types import UserData
from app import SignUpService;

app = Flask(__name__)

signupService = SignUpService()

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/signup")
def signup(name = None):
    return render_template(
        "index.html",
        name=name
    )

@app.route("/signin")
def signin(name = None):
    return render_template(
        "signin.html",
        name=name
    )


@app.route("/api/signup", methods=['POST'])
def signupapi():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        print(username, password)
        userdata = UserData(username, password)

        return signupService.signup(userdata)
    else:
        return "methon is not POST"