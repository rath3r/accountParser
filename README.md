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

## Process

### MVP

- Add each line of the csv to a db table
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

```

```
