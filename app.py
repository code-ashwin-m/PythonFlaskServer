from flask import Flask
from flask import render_template
from flask import request
from system.types import UserData
from system import UserService;
import json 

app = Flask(__name__,
    static_url_path='', 
    static_folder='web/static',
    template_folder='web/templates')

user_service = UserService()

@app.route("/")
def home(name = None):
    return render_template(
        "index.html",
        name=name
    )

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
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        userdata = UserData(None, email, password, name, 0)
    
        try:
            new_user = user_service.signup(userdata)
            jsonstr = json.dumps(new_user.__dict__) 
            return jsonstr
        except Exception as ex:
            return {
                "error": str(ex)
            }
    else:
        return "methon is not POST"