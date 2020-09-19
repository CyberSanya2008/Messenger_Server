from flask import Blueprint, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
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
        return redirect('/')

    # Добавление Пользователя, если email не существует в бд
    new_user = new_user = User(
        email=email, name=name, password=generate_password_hash(password))

    db.session.add(new_user)
    db.session.commit()

    print(data)

    return 'registration'


@main.route('/login', methods=['POST'])
def login_post():
    data = request.data
    parsed_data = json.loads(data)

    email = parsed_data['email']
    password = parsed_data['password']
    checkbox = parsed_data['checkbox']

    if checkbox == "True":
        remember = True
    else:
        remember = False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        print("not")
        return redirect('/')

    login_user(user, remember=remember)
    return redirect('/profile')

    # print(email, password, checkbox)

    return ""


@main.route('/profile')
@login_required
def profile():
    return ("jopa")
