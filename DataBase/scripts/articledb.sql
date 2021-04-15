DROP SCHEMA IF EXISTS articledb CASCADE;

CREATE SCHEMA articledb;
SET search_path TO articledb;

---------------------- ArticleDB Schema Creation --------------------------

CREATE TABLE Article(
article_id integer PRIMARY KEY,
title text NOT NULL,
abstract text NOT NULL
);

CREATE TABLE Author(
	author text,
	title text NOT NULL,
	publication_date Timestamp NOT NULL
);

CREATE TABLE Abstract(
	abstract_d integer PRIMARY KEY,
	abst text NOT NULL
);

------------------- ArticleDB Data Loading -------------------------------


--\copy Article from PROGRAM 'curl https://storage.googleapis.com/psql_bucket/tablesfolder/Artist.csv' DELIMITER ',' CSV;

-- The following commands will load (copy) the data from a public URL
-- Tip: Execute the copy statements one by one and verify that the data has been
-- successfully loaded every time (no error messages appear and table tuples are
-- populated successfully!)


-- COPY Article(article_id, title, abstract)
-- FROM PROGRAM '/home/Panda21/Documents/Emory/2020 - 2021/Spring 2021/CS 329/NewsChain Project/venv/Article'
-- DELIMITER ','
-- CSV HEADER;

-- COPY Author(author, title, publication_date)
-- FROM PROGRAM '/home/Panda21/Documents/Emory/2020 - 2021/Spring 2021/CS 329/NewsChain Project/venv/Author'
-- DELIMITER ','
-- CSV HEADER;

-- COPY Abstract(abstract_id, abst)
-- FROM PROGRAM '/home/Panda21/Documents/Emory/2020 - 2021/Spring 2021/CS 329/NewsChain Project/venv/Abstract'
-- DELIMITER ','
-- CSV HEADER;


