from flask import Blueprint, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Messages
from . import db
import json

main = Blueprint('main', __name__)


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

        l = []

        for i in range(len(messages)):
            usertest = User.query.filter_by(id=messages[i].sender_id).first()
            l.append(usertest.email)

        return json.dumps(l)

    return "Error"


# Поиск Пользователей
@main.route('/<user_email>/<user_password>/users/<search>')
def find_user(user_email, user_password, search):
    user = User.query.filter_by(email=user_email).first()
    if user and check_password_hash(user.password, password=user_password):
        # Если успех
        find_user = User.query.filter(User.email.like('%'+search+'%')).all()
        print(len(find_user))

        l = []

        for i in range(len(find_user)):

            l.append(find_user[i].email)

        return json.dumps(l)

    return "Error"
