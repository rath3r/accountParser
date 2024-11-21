from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from accountParser.db import get_db

class file():
    def __init__(self, name, location):
        self.name = name
        self.location = location

bp = Blueprint('home', __name__, url_prefix='/')

def getCategoryByTime(month, year):
    db = get_db()
    categories = db.execute(
        '''
        SELECT SUM(accountEntries.amount) AS amount, categories.title 
        FROM accountEntries 
        JOIN categories ON accountEntries.category_id=categories.id 
        WHERE accountEntries.month = ? AND accountEntries.year = ? 
        GROUP BY category_id
        ''',
        (month, year,)
    ).fetchall()
    return categories

@bp.route('/', methods=('GET', 'POST'))
def files():
    categories = []
    month = False
    year = False
    if request.args.get("month") or request.args.get('year'):
        if not request.args.get('month') == 'month':
            month = request.args.get('month')
        if not request.args.get('year') == 'year':
            year = request.args.get('year')
        print(month)
        categories = getCategoryByTime(month, year)
        print(categories)
        
    return render_template('home/index.html', categories=categories)
