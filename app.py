from flask import Flask
from flask import render_template, make_response, jsonify
from flask import request
from system.types import UserData
from system import UserService
import json 

app = Flask(__name__,
    static_url_path='', 
    static_folder='web/static',
    template_folder='web/templates')

user_service = UserService()

if __name__ == '__main__':
    app.run(debug=True)
    
def token_required(f):
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return jsonify({'error': 'token is missing'}), 403
        try:
            user_service.security_check(token)
        except Exception as ex:
            return {
                "error": str(ex)
            }, 400
        return f(*args, **kwargs)
    return decorated

@app.route("/")
def home():
    return render_template(
        "home.html",
        data=json.dumps(UserData(None, '', '', 'Hai', '', '').__dict__)
    )

@app.route("/api/signup", methods=['POST'])
def signupapi():
    if request.method == 'POST':
        data = request.get_json();
        name = data.get('name', '')
        email = data.get('email', '')
        password = data.get('password', '')
        role = 2
        if (data.get('student', False) == True):
            role =  1

        userdata = UserData(None, email, password, name, role)
    
        try:
            new_user = user_service.signup(userdata)
            jsonstr = json.dumps(new_user.__dict__) 
            return jsonstr
        except Exception as ex:
            return {
                "error": str(ex)
            }, 400
    else:
        return "method is not POST"
    
@app.route("/api/login", methods=['POST'])
def signinapi():
    if request.method == 'POST':
        data = request.get_json();
        email = data.get('email', '')
        password = data.get('password', '')

        userdata = UserData(None, email, password, None, None)
        
        try:
            sign_in_data = user_service.signin(userdata)
            jsonstr = json.dumps(sign_in_data['user'].__dict__) 
            resp = make_response(jsonstr)
            resp.set_cookie('token', sign_in_data['security'].token)
            return resp
        except Exception as ex:
            return {
                "error": str(ex)
            }, 400
        
    else:
        return "method is not POST"

@app.route("/api/logut", methods=['POST'])
def signoutapi():
    if request.method == 'POST':
        
        try:
            token = request.cookies.get('token')
            sign_out_data = user_service.signout(token)
            resp = make_response("{\"status\": true}")

            if (sign_out_data == True):
                resp.delete_cookie('token')
            return resp
        except Exception as ex:
            return {
                "error": str(ex)
            }, 400
        
    else:
        return "method is not POST"
    
@app.route("/api/user/info")
@token_required
def get_user_info():
    try:
        token = request.cookies.get('token')
        user = user_service.get_user_info_by_token(token)
        jsonstr = json.dumps(user.__dict__) 
        return jsonstr
    except Exception as ex:
        return {
            "error": str(ex)
        }, 400