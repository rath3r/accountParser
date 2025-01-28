/*
Possible future tables
files - to list processed files
*/

DROP TABLE IF EXISTS accountEntries;
DROP TABLE IF EXISTS fileTypes;
DROP TABLE IF EXISTS files;

CREATE TABLE accountEntries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    amount INTEGER,
    file_id INTEGER,
    category_id INTEGER,
    dateAdded INTEGER,
    dateUpdated INTEGER,
    date TEXT,
    year INTEGER,
    month INTEGER
);

CREATE TABLE categories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL
);

CREATE TABLE fileTypes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT,
  entryDescription TEXT,
  entryAmount TEXT,
  entryDate TEXT,
  entryDateFormat TEXT
);

CREATE TABLE files (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  dateUploaded TEXT,
  dateUpdated TEXT,
  processed INTEGER,
  fileType_id INTEGER
);
