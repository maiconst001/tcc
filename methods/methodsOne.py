
from random import choice, randint
import jwt, datetime, os
from PIL import Image
import os


abc = 'a,_,1,&,b,2,@,c,3,d,4,e,5,f,_,6,g,7,h,8,i,9,j,0,k,l,m,n, o, p, q, r, s, t, u, v, w, x, y, z'
abc = abc.replace(' ','').split(',')


def resizeImage(img, size=(250,250)):
    dir_save = img

    im = Image.open(img)
    im.thumbnail(size, Image.ANTIALIAS)
    im.save(dir_save, quality=50)


def gerate_image(base, length=30):
    _id = ''
    while True:
        for c in range(length):
            i = choice(abc)
            _id += str(i)

        if base.query.filter_by(banner=_id).first():
            _id = ''
        else: 
            break
    return _id.strip()


def gerate_aba_id(base, length=30):
    _id = ''
    while True:
        for c in range(length):
            i = choice(abc)
            _id += str(i)

        if base.query.filter_by(id_sec=_id).first():
            _id = ''
        else: 
            break
    return _id.strip()


def verify_login(email, password, base):
    b = base.query.filter_by(email=email, password=password).first()
    if b:
        return True
    return False


def gerate_token(email, password, secret):
    payload = {
        'email': email,
        'password': password,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=50 * 10)
    }

    token = jwt.encode(payload, secret)
    return {
        'verified': True,
        'date': datetime.datetime.utcnow(),
        'token': token,
    }


def verify_token(token, secret, base):
    try:
        token = jwt.decode(token, secret, algorithms="HS256")
        email = token['email']
        senha = token['password']

        if verify_login(email, senha, base):
            return {
                'status': True,
                'token': token
            }
        return {
            'status': False
        }
    except Exception as erro:
        return {
            'status': False
        }











def delete(email, id, base, product, db, dirimg):
    user = base.query.filter_by(email=email).first()
    iduser = user.id

    obj = product.query.filter_by(id=id, id_ref=iduser).first()

    try:
        os.remove(dirimg + '/' +obj.banner + '.WEBP')
    except:
        pass
    db.session.delete(obj)
    db.session.commit()



