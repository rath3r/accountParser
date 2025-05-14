from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from accountParser.db import get_db
from accountParser.categories import getCategories
import json
import calendar

from datetime import datetime

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
    years = [2024, 2025]

    currentMonth = int(datetime.today().strftime('%-m'))
    currentYear = int(datetime.today().strftime('%Y'))
    monthsToGet = []
    print(currentMonth - 1)
    targetMonth = currentMonth
    targetYear = currentYear
    for i in range(1, 13):
        target = []
        targetMonth = targetMonth - 1
        if(targetMonth == 0):
            targetMonth = 12
            targetYear = targetYear - 1
        target.append(targetMonth)
        target.append(targetYear)
        target.append(calendar.month_abbr[targetMonth])
        monthsToGet.append(target)
    
    print(monthsToGet)

    for x in reversed(monthsToGet):
        print(x)
    
    for category in getCategories():
        categoryArr = []
        categoryArr.append(category['title'])
        for i in reversed(monthsToGet):
            #print(i)
            monthSum = getCatSumByIDandTime(category['id'], i[0], i[1])
            #print(monthSum[0]['amount'])
            if not monthSum[0]['amount']:
                categoryArr.append(0)
            else:
                categoryArr.append("{:.2f}".format(monthSum[0]['amount']))
        
        firstHalf = 0
        for i in range(1, 6):
            firstHalf += float(categoryArr[i])
        #categoryArr.append("{:.2f}".format((firstHalf/6)))

        secondHalf = 0
        for i in range(7,13):
            secondHalf += float(categoryArr[i])
        #categoryArr.append("{:.2f}".format((secondHalf/6)))

        lastThree = 0
        for i in range(10,13):
            lastThree += float(categoryArr[i])
        categoryArr.append("{:.2f}".format((lastThree/3)))

        lastSix = 0
        for i in range(7,13):
            lastSix += float(categoryArr[i])
        categoryArr.append("{:.2f}".format((lastSix/6)))

        lastTweleve = 0
        for i in range(1,13):
            lastTweleve += float(categoryArr[i])
        categoryArr.append("{:.2f}".format((lastTweleve/12)))

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
    return render_template('home/index.html', categories=categories, months=reversed(monthsToGet))
