from flask import Flask, request, session, render_template, make_response, redirect, url_for
from services import UserService, ProfileService
from typing import List
import json, calendar

from model import User, Security, TeacherSubject, Availability

app = Flask(__name__,
    static_url_path='', 
    static_folder='web/static',
    template_folder='web/templates')
app.secret_key = 'af48cd8c-b54b-41bf-ab20-6e8b034c9d5d'  # Change this to a random secret key

user_service = UserService()
profile_service = ProfileService()

if __name__ == '__main__':
    app.run(debug=True, host="192.168.1.35", port=8080)
    
def token_required(f):
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return redirect(url_for('web_login'))
        try:
           security = user_service.security_check1(token)
        except Exception as ex:
            return redirect(url_for('web_login'))
        return f(security, *args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated


@app.context_processor
def inject_user_data():
    is_authenticated = None
    if 'user_id' in session:
        is_authenticated = True

    def get_day_names(value: str):
        values = list(value)
        result = []
        for item in values:
            result.append(calendar.day_abbr[int(item)-1])
        print(result)
        return ", ".join(result)
    
    return {
            'is_authenticated': is_authenticated, 
            'site_name': 'My Flask App',
            'get_day_names': get_day_names
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
            _user = User(
                id=None,
                email=email, 
                password=password, 
                name=name, 
                role=role
            )
            user_service.signup1(_user)
        except Exception as ex:
            return render_template("register.html", error=ex)
    return render_template("register.html")


@app.route("/api/login", methods=['POST'])
def api_login():
    data = request.get_json();
    email = data.get('email', '')
    password = data.get('password', '')
    try:
        user, security = login1(email, password)
        jsonstr = json.dumps(user.__dict__) 
        resp = make_response(jsonstr)
        resp.headers["Content-Type"] = "application/json; charset=utf-8"
        resp.set_cookie('token', security.token)
        return resp
    except Exception as ex:
        return "{\"error\"=\"" + str(ex) + "\"}"

@app.route("/login", methods=['GET', 'POST'])
def web_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user, security = login1(email, password)
            session['user_id'] = user.id
            resp = make_response(redirect('dashboard'))
            resp.set_cookie('token', security.token)
            return resp
        except Exception as ex:
                return render_template("login.html", error=ex)
    return render_template("login.html")

def login1(email: str, password: str):
    user = User(None, email, password, None, None) 
    user, security = user_service.signin1(user)
    return user, security

@app.route("/api/logout", methods=['POST'])
def api_logout():
    try:
        token = request.cookies.get('token')
        user_service.signout1(token)
        resp = make_response("{\"status\"=\"success\"}")
        resp.headers["Content-Type"] = "application/json; charset=utf-8"
        resp.set_cookie('token', '')
        return resp
    except Exception as ex:
        return "{\"error\"=\"" + str(ex) + "\"}"
    
@app.route("/logout", methods=['GET', 'POST'])
@token_required
def web_logout(security: Security):
    try:
        user_service.signout1(security.token)
        session.pop('user_id', None)
        resp = make_response(redirect(url_for('web_login')))
        resp.set_cookie('token', '')
        return resp
    except Exception as ex:
        return render_template("login.html", error=ex)
    
@app.route("/dashboard")
@token_required
def dashboard(security: Security):
    user: User = user_service.get_user_info_by_id1(security.user_id)
    return render_template("dashboard.html", user=user)

@app.route("/user")
@token_required
def user(security: Security):
    user: User = user_service.get_user_info_by_id1(security.user_id)
    availabilities: List[Availability] = profile_service.get_all_availability_by_user_id1(security.user_id)
    subjects: List[TeacherSubject] = profile_service.get_all_subjects_by_user_id1(security.user_id)
    return render_template(
        "user.html", 
        user=user, 
        availability_list=availabilities,
        subject_list=subjects
    )

@app.route("/subjects")
@token_required
def subjects(security: Security):
    return render_template("subjects.html")

@app.route("/subjects/add", methods=['GET', 'POST'])
@token_required
def subject_add(security: Security):
    if request.method == 'POST':
        subject_id = request.form.get('subject')
        teacher_subjects = TeacherSubject(None, security.user_id, subject_id)
        profile_service.add_subject1(teacher_subjects)
        resp = make_response(redirect(url_for('user')))
        return resp

    subjects = profile_service.get_all_subjects1()
    return render_template("subjects-add.html", subject_list=subjects)

@app.route("/subjects/<int:id>/delete", methods=['GET'])
@token_required
def subject_delete(security: Security, id: int):
    profile_service.delete_subject1(id)
    resp = make_response(redirect('/user'))
    return resp

@app.route("/availability/add", methods=['GET', 'POST'])
@token_required
def availability_add(security: Security):
    if request.method == 'POST':
        start_time = request.form.get('start-time')
        end_time = request.form.get('end-time')
        days = request.form.getlist('days')
        availability = Availability(None, security.user_id, start_time, end_time, "".join(days))
        profile_service.add_availability1(availability)
        resp = make_response(redirect(url_for('user')))
        return resp
    return render_template("availability-add.html")

@app.route("/availability/<int:availability_id>/delete", methods=['GET'])
@token_required
def availability_delete(security: Security, availability_id: int):
    profile_service.delete_availability1(availability_id)
    resp = make_response(redirect('/user'))
    return resp

@app.route("/class/enroll", methods=['GET', 'POST'])
@token_required
def class_enroll(security: Security):
    subject_id = request.args.get('subject')
    if subject_id:
        subject_id = int(subject_id)
    teachers = profile_service.get_all_teachers_by_subject_id1(subject_id)
    subjects = profile_service.get_all_subjects1()
    return render_template("class-enroll.html", subject_id=subject_id, subject_list=subjects, teacher_list=teachers)