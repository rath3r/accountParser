import functools, csv, os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.utils import secure_filename
from accountParser.db import get_db
from datetime import datetime
from accountParser.categories import getCategories

class file():
    def __init__(self, name, location):
        self.name = name
        self.location = location


bp = Blueprint('entries', __name__, url_prefix='/entries')

@bp.route('/')
def index():
    db = get_db()
    entries = db.execute(
        'SELECT * FROM accountEntries'
    ).fetchall()

    return render_template('entries/index.html', entries=entries)
