from flask import Flask
from flask import render_template, make_response, jsonify, redirect, url_for, session
from flask import request
from models import AppData, UserDto, SecurityDto

from system import UserService
import json 

app = Flask(__name__,
    static_url_path='', 
    static_folder='web/static',
    template_folder='web/templates')
app.secret_key = 'af48cd8c-b54b-41bf-ab20-6e8b034c9d5d'  # Change this to a random secret key

user_service = UserService()

if __name__ == '__main__':
    app.run(debug=True)
    
def token_required(f):
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return redirect(url_for('login'))
        try:
           security_dto = user_service.security_check(token)
        except Exception as ex:
            return redirect(url_for('login'))
        return f(security_dto, *args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated


@app.context_processor
def inject_user_data():
    is_authenticated = None
    if 'user_id' in session:
        is_authenticated = True
    return {
            'is_authenticated': is_authenticated, 
            'site_name': 'My Flask App'
        }

@app.route("/")
def index():
    return render_template("base.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = int(request.form.get('role'))

        try:
            user_dto = UserDto(None, email, password, name, role) 
            new_user = user_service.signup(user_dto)
                
        except Exception as ex:
            return render_template("register.html", error=ex)
    return render_template("register.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            user_dto = UserDto(None, email, password, None, None) 
            sign_in_data = user_service.signin(user_dto)
            session['user_id'] = sign_in_data['user'].id
            resp = make_response(redirect('dashboard'))
            resp.set_cookie('token', sign_in_data['security'].token)
            
            return resp
        except Exception as ex:
            return render_template("login.html", error=ex)
    return render_template("login.html")

@app.route("/logout", methods=['GET', 'POST'])
@token_required
def logout(security_dto: SecurityDto):
    try:
        sign_out_data = user_service.signout(security_dto.token)
        session.pop('user_id', None)
        resp = make_response(redirect('login'))
        resp.set_cookie('token', '')
        return resp
    except Exception as ex:
        return render_template("login.html", error=ex)
    
@app.route("/dashboard")
@token_required
def dashboard(security_dto: SecurityDto):
    user_dto: UserDto = user_service.get_user_info_by_id(security_dto.user_id)
    app_data = AppData()
    app_data.user = user_dto
    return render_template("dashboard.html", data=app_data)

@app.route("/user")
@token_required
def user(security_dto: SecurityDto):
    user_dto: UserDto = user_service.get_user_info_by_id(security_dto.user_id)
    app_data = AppData()
    app_data.user = user_dto
    return render_template("user.html", data=app_data)


    