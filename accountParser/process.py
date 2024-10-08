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


bp = Blueprint('process', __name__, url_prefix='/process')

ALLOWED_EXTENSIONS = {'csv'}
UPLOAD_FOLDER = '/home/thomas/sites/projects/accountsParser/uploads'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getFileTypes():
    db = get_db()
    fileTypes = db.execute(
        'SELECT * FROM fileTypes'
    ).fetchall()
 
    return fileTypes

def readEntryCSV(filename):
    lines = []
    uploadsPath = f"{os.getcwd()}/uploads"
    try:
        with open(f"{uploadsPath}/{filename}") as csvfile:
            fileReader = csv.reader(csvfile)
            for row in fileReader:
                lines.append(row)
    except FileNotFoundError:
        print(f"{filename}: does not exist")

    return lines

def getFileByID(id):
    db = get_db()
    file = db.execute(
        'SELECT * FROM files WHERE files.id = ?',
        (id)
    ).fetchone()

    return file

def getFileTypeById(id):
    db = get_db()
    fileType = db.execute(
        'SELECT * FROM fileTypes WHERE fileTypes.id = ?',
        (id,)
    ).fetchone()

    return fileType

def checkForEntriesByFile(id):
    db = get_db()
    count = db.execute(
        'SELECT COUNT() FROM accountEntries WHERE accountEntries.file_id = ?',
        (id,)
    ).fetchone()

    if count[0] > 0:
        check = True
    else:
        check = False

    return check

def getEntriesByFileID(id):
    db = get_db()
    entries = db.execute(
        'SELECT * FROM accountEntries WHERE accountEntries.file_id = ?',
        (id,)
    ).fetchall()

    return entries

@bp.route('/')
def index():

    return render_template('process/index.html')

@bp.route('/files', methods=('GET', 'POST'))
def files():
    if request.method == 'POST':
        # check if the post request has the file part
        print("files")

        if 'file' not in request.files:
            flash('No file part')

            return redirect(request.url)
        
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            
            title = filename
            date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

            db = get_db()
            db.execute(
                'INSERT INTO files (title, dateUploaded)'
                ' VALUES (?, ?)',
                (title, date,)
            )
            db.commit()
            
            return redirect('/process/files')
        else:
            flash('File type not supported')

            return redirect(request.url)
    
    db = get_db()
    files = db.execute(
        'SELECT * FROM files'
    ).fetchall()
    
    return render_template('process/files.html', files=files)

# process an individual file 
# the name could be the actual file name initially and the file name as recorded in the 
@bp.route('/file', methods=('GET', 'POST'))
def processFile():
    lines = []
    fileTypes = []
    db = get_db()
    if request.method == 'POST':
        # deal with the form
        # deal with the File Type
        title = request.form['fileTypeTitle']
        entryDescription = request.form['entryDescription']
        entryAmount = request.form['entryAmount']
        fileID = request.form['fileID']
        
        try:
            fileTypeID = request.form['fileTypeID']
        except:
            fileTypeID = False

        print(fileTypeID)

        if not fileTypeID:
            
            db.execute(
                'INSERT INTO fileTypes (title, entryDescription, entryAmount)'
                ' VALUES (?, ?, ?)',
                (title, entryDescription, entryAmount,)
            )
            db.commit()
            
            fileType = db.execute(
                'SELECT id FROM fileTypes WHERE fileTypes.title = ?',
                (title,)
            ).fetchone()
            fileTypeID = fileType['id']
        
        db.execute(
            'UPDATE files SET fileType_id = ? WHERE id = ?',
            (fileTypeID, fileID)
        )
        db.commit()

        return redirect('/process/files')
    else:
        file = getFileByID(request.args.get('fileID'))
        lines = readEntryCSV(file['title'])
        fileTypes = getFileTypes()

    return render_template('process/file.html', file=file, lines=lines, fileTypes=fileTypes)

@bp.route('/entries', methods=('GET', 'POST'))
def processEntries():
    if request.method == 'POST':
        #print(request.form)
        fileID = request.form.get('fileID')
        entriesArr = []
        for i, input in enumerate(request.form):
            if str(i) + "-date" in request.form:
                rowDict = {}
                rowDict['date'] = request.form.get(str(i) + "-date")
                rowDict['description'] = request.form.get(str(i) + "-description")
                rowDict['amount'] = request.form.get(str(i) + "-amount")
                entriesArr.append(rowDict)

        #print(entriesArr)
        for entry in entriesArr:
            if entry['amount'] == '':
                amount = 0
            else:
                amount = abs(float(entry['amount']))

            db = get_db()
            db.execute(
                'INSERT INTO accountEntries (description, amount, file_id, dateAdded, dateUpdated, date)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (entry['description'], amount, fileID, datetime.now(), datetime.now(), entry['date'])
            )
            db.commit()

        return redirect('/entries')

    else:
        fileID = request.args.get('fileID')
        file = getFileByID(fileID)
        fileProcessed = checkForEntriesByFile(fileID)
        lines = readEntryCSV(file['title'])
        categories = getCategories()
        fileTypeID = file['fileType_id']
        fileType = getFileTypeById(fileTypeID)
        entriesArr = []

        descriptionIndex = 0
        amountIndex = 0
        entryDate = 0
        for i, line in enumerate(lines):
            if i == 0:
                for j, el in enumerate(line):
                    if el == fileType['entryDescription']:
                        descriptionIndex = j
                    if el == fileType['entryAmount']:
                        amountIndex = j
                    if el == fileType['entryDate']:
                        entryDate = j
            else:
                lineArr = []
                lineArr.append(line[entryDate])
                lineArr.append(line[descriptionIndex])
                lineArr.append(line[amountIndex])
                entriesArr.append(lineArr)

    # check if this file has entries in the accountEntries table

    # handle the submit by adding the categories

    return render_template('process/entries.html', file=file, fileProcessed=fileProcessed, lines=entriesArr, categories=categories)


@bp.route('/categorize', methods=('GET', 'POST'))
def categorizeEntries():
    fileID = request.args.get('fileID')
    file = getFileByID(fileID)
    categories = getCategories()
    fileProcessed = checkForEntriesByFile(fileID)
    lines = []
    print(checkForEntriesByFile(fileID))
    if checkForEntriesByFile(fileID):
        entries = getEntriesByFileID(fileID)
        print(entries)

        test = "test"
    

    return render_template('process/categorize.html', file=file, fileProcessed=fileProcessed, lines=entries, categories=categories)
