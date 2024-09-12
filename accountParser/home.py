from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from accountParser.db import get_db

class file():
    def __init__(self, name, location):
        self.name = name
        self.location = location

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/', methods=('GET', 'POST'))
def files():

    return render_template('home/index.html')
