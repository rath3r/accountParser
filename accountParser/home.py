from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from accountParser.db import get_db
from accountParser.categories import getCategories
import json

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

def getCatSumByIDandTime(id, month, year):

    db = get_db()
    categorySum = db.execute(
         '''
        SELECT SUM(accountEntries.amount) AS amount 
        FROM accountEntries 
        JOIN categories ON accountEntries.category_id=categories.id 
        WHERE accountEntries.month = ? AND accountEntries.year = ? AND accountEntries.category_id = ?
        ''',
        (month, year, id)
    ).fetchall()
    return categorySum

@bp.route('/', methods=('GET', 'POST'))
def files():
    categoriesObj = { "categories": [] }
    categories = []
    #print(getCategories())
    for category in getCategories():
        categoryArr = []
        categoryArr.append(category['title'])
        for i in range(1, 13):
            print(i)
            monthSum = getCatSumByIDandTime(category['id'], i, 2024)
            #print(monthSum[0]['amount'])
            if not monthSum[0]['amount']:
                categoryArr.append(0)
            else:
                categoryArr.append("{:.2f}".format(monthSum[0]['amount']))
        firstHalf = 0
        for i in range(1, 6):
            firstHalf += float(categoryArr[i])
        categoryArr.append("{:.2f}".format((firstHalf/6)))

        secondHalf = 0
        for i in range(7,13):
            secondHalf += float(categoryArr[i])
        categoryArr.append("{:.2f}".format((secondHalf/6)))

        categories.append(categoryArr)


    '''
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
    '''
    return render_template('home/index.html', categories=categories)
