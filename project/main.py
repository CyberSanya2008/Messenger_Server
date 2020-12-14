from flask import Blueprint, request, redirect, Flask
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Messages, Dialogs
from . import db
from . import socketio
from flask_socketio import send
import json
from sqlalchemy import or_

main = Blueprint('main', __name__)


@socketio.on('message')
def handleMessage(msg):
    print('MEssage: +' + msg)
    send(msg, broadcast=True)

@main.route('/')
def index():
    data = request.data
    print(data)

    return 'index'


# Регистрация пользователя и добавление его в базу данных
@main.route('/registration', methods=['POST'])
def registration():

    data = request.data
    parsed_data = json.loads(data)

    email = parsed_data['email']
    name = parsed_data['name']
    password = parsed_data['password']

    # Проверка email
    user = User.query.filter_by(email=email).first()
    if user:
        return "Error"

    # Добавление Пользователя, если email не существует в бд
    new_user = new_user = User(
        email=email, name=name, password=generate_password_hash(password))

    db.session.add(new_user)
    db.session.commit()

    print(data)

    return 'registration'


@main.route('/sendmessage', methods=["POST"])
def sendmessage():
    data = request.data
    parsed_data = json.loads(data)

    reciever = parsed_data['reciever']
    sender = parsed_data['sender']
    message_text = parsed_data['message_text']

    user = User.query.filter_by(email=reciever).first()
    sender_user = User.query.filter_by(email=sender).first()

    new_message = Messages(
        text=message_text, sender_id=sender_user.id, receiver_id=user.id)

    db.session.add(new_message)
    db.session.commit()

    return "Ok"

#  Вывод данных пользователя при правильном логине и пароле


@main.route('/profile/<user_email>/<user_password>')
def profile(user_email, user_password):

    user = User.query.filter_by(email=user_email).first()

    # Проверка email и пароля
    if user and check_password_hash(user.password, password=user_password):
        # Если успех
        return user.name
    # Если ошибка
    return "Error"


@main.route('/profile/messages/<user_email>/<user_password>')
def showMessages(user_email, user_password):
    user = User.query.filter_by(email=user_email).first()

    if user and check_password_hash(user.password, password=user_password):
        # Если успех
        messages = Messages.query.filter_by(receiver_id=user.id).all()

        for i in messages:
            print(i.text)

        print('jopa')
        print(messages[0].text)
        print(len(messages))

        return messages[2].text

    return "Error"


@main.route('/profile/dialogs/<user_email>/<user_password>')
def showDialogs(user_email, user_password):
    user = User.query.filter_by(email=user_email).first()
    if user and check_password_hash(user.password, password=user_password):
        # Если успех

        messages = Messages.query.filter_by(receiver_id=user.id).all()
        dialogs1 = Dialogs.query.filter_by(user1=user.email).all()
        dialogs2 = Dialogs.query.filter_by(user2=user.email).all()
        # dialogs = Dialogs.query.filter_by(or_(Dialogs.user1==user_email), Dialogs.user2==user_email).all
        l = []
        for i in dialogs1:
            l.append(i.user2)

        for i in dialogs2:
            l.append(i.user1)
        print(l)

        return json.dumps(l)

    return "Error"


# Поиск Пользователей по почте
@main.route('/<user_email>/<user_password>/users/<search>')
def find_user(user_email, user_password, search):
    user = User.query.filter_by(email=user_email).first()
    if user and check_password_hash(user.password, password=user_password):
        # Если успех
        find_user = User.query.filter(User.email.like(
            '%'+search+'%')).order_by(User.email).all()
        print(len(find_user))

        l = []

        for i in range(len(find_user)):

            if find_user[i].email.startswith(search):
                l.append(find_user[i].email)

        for i in range(len(find_user)):

            if not find_user[i].email.startswith(search):
                l.append(find_user[i].email)

        return json.dumps(l)

    return "Error"


# Добавление диалогов
@main.route('/create-dialog', methods=['POST'])
def create_dialog():

    data = request.data
    parsed_data = json.loads(data)

    user1 = parsed_data['user1']
    user2 = parsed_data['user2']

    # # Проверка email
    # user = User.query.filter_by(email=email).first()
    # if user:
    #     return "Error"

    # Добавление диалога
    new_dialog = Dialogs(user1=user1, user2=user2)

    db.session.add(new_dialog)
    db.session.commit()

    print(data)

    return 'registration'
