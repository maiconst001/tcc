from flask import Blueprint, current_app, render_template, request, redirect, url_for, current_app, jsonify
from database import User

from methods.methodsOne import verify_token




Vue = Blueprint('vue', __name__, template_folder='templates', static_folder='dist', static_url_path="/tcc")



@Vue.route('/tcc/', defaults={'path': ''})
def catch_all(path):
    token = request.cookies.get('token')

    very = verify_token(token, current_app.config['SECRET_KEY'], User)
    if very['status']:
        return Vue.send_static_file("index.html")
    return redirect('/login')



@Vue.route('/tcc/<path>')
def red(path):
    token = request.cookies.get('token')

    very = verify_token(token, current_app.config['SECRET_KEY'], User)
    if very['status']:
        return Vue.send_static_file("index.html")
    return redirect('/login')

