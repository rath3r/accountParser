import functools, csv, os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from accountParser.db import get_db

class file():
    def __init__(self, name, location):
        self.name = name
        self.location = location

bp = Blueprint('auth', __name__, url_prefix='/process')

@bp.route('/files', methods=('GET', 'POST'))
def files():
    if request.method == 'POST':
        # some post code
        temp = "text"
    
    # need to get the files from somewhere
    files = [
        [['title', 'hello']],
        [['title', 'wrong']]
    ]

    return render_template('process/files.html', files=files)

# process an individual file 
# the name could be the actual file name initially and the file name as recorded in the 
# example file 9e6295b0-2d43-4578-9968-6f5233699060.csv
@bp.route('/file/<filename>')
def processFile(filename):
    uploadsPath = f"{os.getcwd()}/uploads"

    lines = []
    try:
        with open(f"{uploadsPath}/{filename}") as csvfile:
            fileReader = csv.reader(csvfile)
            for row in fileReader:
                # print(', '.join(row))
            #    line = []
                lines.append(row)

#                print(line)
#            lines.append(row)
    except FileNotFoundError:
        print(f"{filename}: does not exist")

    print(lines)
    return render_template('process/file.html', file=filename, lines=lines)