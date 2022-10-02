from flask import Blueprint, render_template, request, redirect, url_for, current_app, jsonify
from methods.methodsOne import verify_login, gerate_token, verify_token, gerate_image
from database import User


Login = Blueprint('login', __name__, template_folder='templates')



@Login.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    user = User(
        username = 'maicon store',
        email = 'videos2018pg@gmail.com',
        password = 'maicon2018',
        verified_acount = True,
    )
    current_app.db.session.add(user)
    current_app.db.session.commit()

    return 'created'



@Login.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST': # verifica se o metodo é do tipo post
        email = request.form.get('email')
        password = request.form.get('password')

        if email and password: # verifica se tem uma senha e um password
            if verify_login(email, password, User): # verifica se o usuario e a senha estão no banco
                token = gerate_token(email, password, current_app.config['SECRET_KEY'])
                return jsonify(token)

        return jsonify({
            'token': False
        })
    return render_template('login.html')




@Login.route('/verify', methods=['POST'])
def verify():
    if request.method == 'POST': # verifica se o metodo é do tipo post
        token = request.form.get('token')
        print(token)
        if token:
            if verify_token(token, current_app.config['SECRET_KEY'], User)['status']:
                return jsonify({
                    'verified': True,
                    'token': True
                })

    return jsonify({
        'verified': True,
        'token': False
    })