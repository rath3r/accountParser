/*
Possible future tables
files - to list processed files
*/

DROP TABLE IF EXISTS accountEntries;
/*
DROP TABLE IF EXISTS files;
*/

CREATE TABLE accountEntries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    amount INTEGER,
    file_id INTEGER,
    category_id INTEGER,
    dateAdded INTEGER,
    dateUpdated INTEGER
);

/*
CREATE TABLE files (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  dateUploaded TEXT,
  dateUpdated TEXT,
  type TEXT,
  processed INTEGER
);
*/

CREATE TABLE fileTypes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT
)
/*
CREATE TABLE categories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL
)
*/


/*

Original example:

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
*/

