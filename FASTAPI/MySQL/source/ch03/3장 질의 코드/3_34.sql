CREATE TABLE	NewBook (
  bookid		INTEGER, 
  bookname		VARCHAR(20),
  publisher		VARCHAR(20),
  price		INTEGER);

  /*
drop table newbook;
  
  CREATE TABLE	NewBook (
  bookid		INTEGER,
  bookname		VARCHAR(20),
  publisher		VARCHAR(20),
  price		INTEGER,
  PRIMARY KEY	(bookid));

drop table newbook;
  
  CREATE TABLE	NewBook (
  bookid		INTEGER	PRIMARY KEY,
  bookname		VARCHAR(20),
  publisher		VARCHAR(20),
  price		INTEGER);
  
drop table newbook;

CREATE TABLE 	NewBook (
  bookname		VARCHAR(20),
  publisher		VARCHAR(20),
  price 		INTEGER,
  PRIMARY KEY	(bookname, publisher));
  
drop table newbook;


CREATE TABLE 	NewBook (
  bookname		VARCHAR(20)	NOT NULL,
  publisher		VARCHAR(20)	UNIQUE,
  price		INTEGER DEFAULT 10000 CHECK(price > 1000),
  PRIMARY KEY	(bookname, publisher));
  */
  
  