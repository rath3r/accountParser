from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from accountParser.db import get_db

class file():
    def __init__(self, name, location):
        self.name = name
        self.location = location

bp = Blueprint('categories', __name__, url_prefix='/categories')

@bp.route('/', methods=('GET', 'POST'))
def files():
    db = get_db()
    categories = db.execute(
        'SELECT * FROM categories'
    ).fetchall()

    return render_template('categories/index.html', categories=categories)

@bp.route('/add', methods=('GET', 'POST'))
def addCategory():
    error = False
    if request.method == 'POST':
        # some post code
        temp = "text"
        #title = request.form['categoryTitle']
        title = request.form.get('categoryTitle')
        if title == '':
            error = True
            
            return render_template('categories/add.html', error=error)

        db = get_db()
        db.execute(
            'INSERT INTO categories (title)'
            ' VALUES (?)',
            (title,)
        )
        db.commit()

        return redirect('/categories')

    return render_template('categories/add.html', error=error)
