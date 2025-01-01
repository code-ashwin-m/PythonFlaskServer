from flask import Flask, request, session, render_template, make_response, redirect, url_for
from models import UserDto, SecurityDto, AvailabilityDto, TeacherSubjectDto
from services import UserService, ProfileService
from typing import List
import json, calendar

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
            user_dto = UserDto(None, email, password, name, role) 
            new_user = user_service.signup(user_dto)
                
        except Exception as ex:
            return render_template("register.html", error=ex)
    return render_template("register.html")


@app.route("/api/login", methods=['POST'])
def api_login():
    data = request.get_json();
    email = data.get('email', '')
    password = data.get('password', '')
    try:
        sign_in_data = login(email, password)
        jsonstr = json.dumps(sign_in_data) 
        # return jsonstr, 200, {'Content-Type': 'application/json; charset=utf-8'}
        resp = make_response(jsonstr)
        resp.headers["Content-Type"] = "application/json; charset=utf-8"
        resp.set_cookie('token', sign_in_data['security']['token'])
        return resp
    except Exception as ex:
        return "{\"error\"=\"" + str(ex) + "\"}"

@app.route("/login", methods=['GET', 'POST'])
def web_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            sign_in_data = login(email, password)
            session['user_id'] = sign_in_data['user']['id']
            resp = make_response(redirect('dashboard'))
            resp.set_cookie('token', sign_in_data['security']['token'])
            return resp
        except Exception as ex:
            return render_template("login.html", error=ex)
    return render_template("login.html")

def login(email: str, password: str):
    user_dto = UserDto(None, email, password, None, None) 
    sign_in_data = user_service.signin(user_dto)
    return sign_in_data

@app.route("/api/logout", methods=['POST'])
def api_logout():
    try:
        token = request.cookies.get('token')
        sign_out_data = user_service.signout(token)
        resp = make_response("{\"status\"=\"success\"}")
        resp.headers["Content-Type"] = "application/json; charset=utf-8"
        resp.set_cookie('token', '')
        return resp
    except Exception as ex:
        return "{\"error\"=\"" + str(ex) + "\"}"
    
@app.route("/logout", methods=['GET', 'POST'])
@token_required
def web_logout(security_dto: SecurityDto):
    try:
        sign_out_data = user_service.signout(security_dto.token)
        session.pop('user_id', None)
        resp = make_response(redirect(url_for('web_login')))
        resp.set_cookie('token', '')
        return resp
    except Exception as ex:
        return render_template("login.html", error=ex)
    
@app.route("/dashboard")
@token_required
def dashboard(security_dto: SecurityDto):
    user_dto: UserDto = user_service.get_user_info_by_id(security_dto.user_id)
    return render_template("dashboard.html", user=user_dto)

@app.route("/user")
@token_required
def user(security_dto: SecurityDto):
    user_dto: UserDto = user_service.get_user_info_by_id(security_dto.user_id)
    availability_list: List[AvailabilityDto] = profile_service.get_all_availability_by_user_id(security_dto.user_id)
    subject_list: List[TeacherSubjectDto] = profile_service.get_all_subjects_by_user_id(security_dto.user_id)
    return render_template(
        "user.html", 
        user=user_dto, 
        availability_list=availability_list,
        subject_list=subject_list
    )

@app.route("/subjects")
@token_required
def subjects(security_dto: SecurityDto):
    return render_template("subjects.html")

@app.route("/subjects/add", methods=['GET', 'POST'])
@token_required
def subject_add(security_dto: SecurityDto):
    if request.method == 'POST':
        subject_id = request.form.get('subject')

        teacher_subject_dto = TeacherSubjectDto(None, security_dto.user_id, subject_id)
        teacher_subject_dto = profile_service.add_subject(teacher_subject_dto)
        resp = make_response(redirect(url_for('user')))
        return resp

    subject_list = profile_service.get_all_subjects()
    return render_template("subjects-add.html", subject_list=subject_list)

@app.route("/subjects/<int:id>/delete", methods=['GET'])
@token_required
def subject_delete(security_dto: SecurityDto, id: int):
    profile_service.delete_subject(id)
    resp = make_response(redirect('/user'))
    return resp

@app.route("/availability/add", methods=['GET', 'POST'])
@token_required
def availability_add(security_dto: SecurityDto):
    if request.method == 'POST':
        start_time = request.form.get('start-time')
        end_time = request.form.get('end-time')
        days = request.form.getlist('days')
        availability_dto = AvailabilityDto(None, security_dto.user_id, start_time, end_time, "".join(days))
        availability_dto = profile_service.add_availability(availability_dto)
        resp = make_response(redirect(url_for('user')))
        return resp
    return render_template("availability-add.html")

@app.route("/availability/<int:availability_id>/delete", methods=['GET'])
@token_required
def availability_delete(security_dto: SecurityDto, availability_id: int):
    profile_service.delete_availability(availability_id)
    resp = make_response(redirect('/user'))
    return resp

@app.route("/class/enroll", methods=['GET', 'POST'])
@token_required
def class_enroll(security_dto: SecurityDto):
    subject_id = request.args.get('subject')
    if subject_id:
        subject_id = int(subject_id)
    teacher_list = profile_service.get_all_teachers_by_subject_id(subject_id)
    subject_list = profile_service.get_all_subjects()
    return render_template("class-enroll.html", subject_id=subject_id, subject_list=subject_list, teacher_list=teacher_list)