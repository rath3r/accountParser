import functools, csv, os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.utils import secure_filename
from accountParser.db import get_db
from datetime import datetime

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

@bp.route('/')
def index():

    return render_template('process/index.html')

@bp.route('/files', methods=('GET', 'POST'))
def files():
    if request.method == 'POST':
        # check if the post request has the file part
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
    
    db = get_db()
    files = db.execute(
        'SELECT * FROM files'
    ).fetchall()
    
    return render_template('process/files.html', files=files)

# process an individual file 
# the name could be the actual file name initially and the file name as recorded in the 
@bp.route('/file/<filename>', methods=('GET', 'POST'))
def processFile(filename):
    lines = []
    if request.method == 'POST':
        # deal with the form
        print(request.form)
        processed = True

        redirect(url_for('process.files'))
    else:
        uploadsPath = f"{os.getcwd()}/uploads"

        try:
            with open(f"{uploadsPath}/{filename}") as csvfile:
                fileReader = csv.reader(csvfile)
                for row in fileReader:
                    lines.append(row)
        except FileNotFoundError:
            print(f"{filename}: does not exist")

        #for line in lines:
            #line.append(''.join(line))
            #print(hash(joinedRow))
        print(lines[0])
        processed = False

    print(lines)
    return render_template('process/file.html', processed=processed, file=filename, lines=lines)
