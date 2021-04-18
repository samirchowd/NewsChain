DROP SCHEMA IF EXISTS articledb CASCADE;

CREATE SCHEMA articledb;
SET search_path TO articledb;

---------------------- ArticleDB Schema Creation --------------------------

CREATE TABLE Article(
article_id integer PRIMARY KEY NOT NULL,
title text NOT NULL,
abstract text NOT NULL,
author text,
source varchar(200),
time_stamp Timestamp NOT NULL);

------------------- ArticleDB Data Loading -------------------------------


--\copy Article from PROGRAM 'curl https://storage.googleapis.com/psql_bucket/tablesfolder/Artist.csv' DELIMITER ',' CSV;

-- The following commands will load (copy) the data from a public URL
-- Tip: Execute the copy statements one by one and verify that the data has been
-- successfully loaded every time (no error messages appear and table tuples are
-- populated successfully!)


-- COPY Article(article_id, title, abstract, author, source, time_stamp)
-- FROM PROGRAM '/home/Panda21/Documents/Emory/2020 - 2021/Spring 2021/CS 329/NewsChain Project/venv/cleaned_data'
-- DELIMITER ','
-- CSV HEADER;


