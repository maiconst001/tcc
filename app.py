from flask import Flask, jsonify, request, session, redirect, render_template
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import false
from database import db_init, User, Agenda, db, Labs
from methods.methodsOne import delete, verify_token


#blueprints imports
from login.login import Login
from vue.vue import Vue

UPLOAD_FOLDER = 'static/user'


app = Flask(__name__)


app.config['SECRET_KEY'] = '__20200000_knfc)$#%9)(*o12020__2020'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.db = db


app.current_app = app.config['SECRET_KEY']



#blueprints
app.register_blueprint(Login) # area de login 
app.register_blueprint(Vue) # area de vue sigle aplicattion 

CORS(app=app)
db_init(app=app)
Migrate(app=app, db=app.db)



@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.route('/')
def main():
    return redirect('/tcc')




# api de informações 

@app.route('/info-user', methods=['POST', 'GET']) # funcionando
def info():
    token = request.form.get('token')

    very = verify_token(token, app.config['SECRET_KEY'], User)
    if very['status']:
        _ags = User.query.all()
        ags = [{
            'id': x.id,
            'name': x.username,
            'email': x.email,
        } for x in _ags]

        return jsonify({
        'status': True,
        'message': 'Ok!',
        'type': 'sucess',
        'content': ags
    })
    
    return jsonify({
        'status': False,
        'message': 'Erro! Invalid token!',
        'type': 'erro'
    })



#metodos de labs 

@app.route('/labs', methods=['POST', 'GET']) # funcionando
def labs():
    token = request.form.get('token')

    very = verify_token(token, app.config['SECRET_KEY'], User)
    if very['status']:
        _ags = Labs.query.all()
        ags = [{
            'id': x.id,
            'type': x.type,
            'name': x.name,
        } for x in _ags]

        return jsonify({
        'status': True,
        'message': 'Ok!',
        'type': 'sucess',
        'content': ags
    })
    
    return jsonify({
        'status': False,
        'message': 'Erro! Invalid token!',
        'type': 'erro'
    })



@app.route('/new-lab', methods=['POST']) # funcionando
def create():
    token = request.form.get('token')

    type = request.form.get('type')
    name = request.form.get('name')

    very = verify_token(token, app.config['SECRET_KEY'], User)
    if very['status']:
        if (type and name):

            lab = Labs(type=type, name=name)
            db.session.add(lab)
            db.session.commit()


            return jsonify({
                'status': True,
                'message': 'Ok! lab cadastrado com sucesso!',
                'type': 'sucess'
            })

    return jsonify({
        'status': False,
        'message': 'Erro! Invalid token!',
        'type': 'erro'
    })



@app.route('/delete-lab', methods=['POST']) # funcionando
def deletepd():
    token = request.form.get('token')
    lab_id = request.form.get('id')


    very = verify_token(token, app.config['SECRET_KEY'], User)
    if very['status']:
        
        Ag = Labs.query.filter_by(id=lab_id).first()
        db.session.delete(Ag)
        db.session.commit()

        return jsonify({
            'message': 'Ok! Deletado com sucesso',
            'type': 'success',

            'status': True
        })

    return jsonify({
        'message': 'Erro! não foi possivel deletar',
        'type': 'erro',

        'status': False
    })



#metodos de Agenda 
@app.route('/new-agenda', methods=['POST']) # funcioando
def createAgenda():
    token = request.form.get('token')

    lab = request.form.get('lab')
    data = request.form.get('data')
    horarios = request.form.get('horarios')

    very = verify_token(token, app.config['SECRET_KEY'], User)
    if very['status']:

        labsall = Labs.query.all()
        if (not labsall):
            return jsonify({
                'status': False,
                'message': 'Erro! Nenhum lab cadastrado!',
                'type': 'erro'
            })

        Agenda_m = Agenda.query.filter_by(data=data).all()



        for a in Agenda_m:
            if a.horarios in horarios:
                return jsonify({
                    'status': False,
                    'message': 'Erro! Já existe uma data!',
                    'type': 'erro'
                })

        user = User.query.filter_by(email=very['token']['email']).first()
        user_id = user.id
        nome = user.username

        ags_all = []

        for c in eval(horarios): 
            ag = Agenda(user_id=user_id, horarios=str(c), lab=lab, data=data, nome=nome)
            ags_all.append(ag)


        db.session.add_all(ags_all)
        db.session.commit()


        return jsonify({
            'status': True,
            'message': 'Ok! data adicionada com sucesso!',
            'type': 'sucess'
        })

    return jsonify({
        'status': False,
        'message': 'Erro! Invalid token!',
        'type': 'erro'
    })


@app.route('/delete-agenda', methods=['POST']) # funcionando
def deleteAgenda():
    token = request.form.get('token')
    id = request.form.get('id')


    very = verify_token(token, app.config['SECRET_KEY'], User)
    if very['status']:

        user = User.query.filter_by(email=very['token']['email']).first()
        user_id = user.id
        
        Ag = Agenda.query.filter_by(id=id).first()
        if (Ag.user_id == user_id): 
            db.session.delete(Ag)
            db.session.commit()

            return jsonify({
                'message': 'Ok! Deletado com sucesso',
                'type': 'success',

                'status': True
            })
    return jsonify({
        'message': 'Erro! não foi possivel deletar',
        'type': 'erro',

        'status': False
    })


@app.route('/agendas', methods=['POST', 'GET']) # funcionando
def GetAgenda():
    token = request.form.get('token')
    very = verify_token(token, app.config['SECRET_KEY'], User)
    if not very['status']: 
        return jsonify({
            'message': 'Erro! você não está logado!',
            'type': 'erro',

            'status': False
        })

    ags = Agenda.query.all()
    _ags = [{
        'key': x.id,

        'customData': {
            'title': 'maicon tts',    
            'lab': x.lab,
            'horarios': x.horarios,
        },
        
        'dates': x.data,
    } for x in ags]
    return jsonify(_ags)
