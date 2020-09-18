from flask import Blueprint, request
from .models import User, Jopa
from . import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return 'Index'


@main.route('/registration', methods=['POST'])
def registration():
    data = request.data
    print(data)

    return registration


@main.route('/profile')
def profile():
    return 'Profile'
