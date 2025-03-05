# Accounts Parser

An app that allows for the simple categorisation of a months spending.

The input would be a CSV containing all transactions for a month.

Category information would then be gleaned from the descriptions and when a new CSV is inputed
these transactions would be added to the predefined categories.

A dashboard would be created to display monthly and running totals.

## Usage

Activate the environment with:

```
$ . .venv/bin/activate
```

To run a python file use:

```
$ flask --app accountParser run --debug
```

## Goals

- Show totals
- Show change per month
- Show average spend

## Technology

Python and browser based everything else

### Rationale

I haven't done anything in it and it is coming up in work.

### Framework

Flask with an SQLlite DB.

`https://flask.palletsprojects.com/en/3.0.x/installation/`

### Database

SQLlite is being used as its light weight and doesn't need a seperate server

`https://flask.palletsprojects.com/en/3.0.x/patterns/sqlite3/`

After running the virtual environment use:

```
$ flask --app accountParser init-db
```

#### Import data

To import data into a database use the SQLITE data import method.

#### Dev DB

To use a dev database an environment variable can be used.

```
$ export FLASK_DEV_DB=true
```

This uses a [built in Flask feature][Flask ENV config] that allows prefixes END variables to be loaded automatically.

#### SQLite help

Use the `sqlite3` command to access the database on the command line.

```
$ sqlite3 accountparser.sqlite
```

Show tables: `.tables`
Show column names: `.schema <table>`

To dump a db use `https://stackoverflow.com/questions/75675/how-to-dump-the-data-of-some-sqlite3-tables`

#### Categories

Categoris are used to group spending. THe different categories are stored in the SQLlite DB and a
backup us kept in CSV files in the non version controlled data directory.

## Process

### MVP

- Add each line of the csv to a db table
- Categorise each line
- Search for individual things in the table
- produce a result

### Full Steps

- run Flask app
- select csv file
- What type of csv file is it?
  - look at header and guess where date title and amount are
  - Add the file to a db table
- categorise lines add to SQL db
- select next csv
- categerise unknown
- update totals

# Next Steps

- Update uploads page to add date of upload
- Entries fix the date column
- Order entries page
- Homepage update the to include last year\
- Change homepage to last 6 months and 3 months

[Flask ENV config]: https://flask.palletsprojects.com/en/stable/config/#configuring-from-environment-variables
