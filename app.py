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
def index():
    return render_template("base.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return 'POST'
    return render_template("register.html")
