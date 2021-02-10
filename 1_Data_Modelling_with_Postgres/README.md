# Data Modelling with Postgres

This represents the first out of the eight projects in the "Data Engineering Nanodegree" provided by Udacity.

## Summary
The project represents the development of an etl pipeline built to facilitate the analysis of data in a music streaming organisation.


## Motivation - TODO
Practice and apply to a real-world scenario the concepts covered in the 'Data Modelling with Postgres' chapter such as:\
-normalisation/ denormalisation\
-query derivation\
-star schema implementation\
-SQL operations\
-Postgres

## Project Details
### Introduction
A music streaming organisation similar to Spotify has been collecting data on its user's actity while they were using the streaming application. The business analytics team intends to gain insight on the frequency with which songs are played.\
The team requires the engineer to design and develop a database schema and an ETL pipeline optimised for the already collected data and the analysis mentioned above.

### Existing Data - TODO
The existing data consists of two datasets:\

1. Song Dataset\
Descritpion: Contains metadata about songs and their artists.\
Format: JSON\
Partitioned: One song per file.\
File example:\
  {"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}

2. Log Dataset\
Description: Activity details obtained from the music streaming app\
Format: JSON\
Partitioned: One month per file.\
File example:\
  {"artist":null,"auth":"Logged In","firstName":"Walter","gender":"M","itemInSession":0,"lastName":"Frye","length":null,"level":"free","location":"San Francisco-Oakland-Hayward, CA","method":"GET","page":"Home","registration":1540919166796.0,"sessionId":38,"song":null,"status":200,"ts":1541105830796,"userAgent":"\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"","userId":"39"}
  {"artist":null,"auth":"Logged In","firstName":"Kaylee","gender":"F","itemInSession":0,"lastName":"Summers","length":null,"level":"free","location":"Phoenix-Mesa-Scottsdale, AZ","method":"GET","page":"Home","registration":1540344794796.0,"sessionId":139,"song":null,"status":200,"ts":1541106106796,"userAgent":"\"Mozilla\/5.0 (Windows NT 6.1; WOW64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/35.0.1916.153 Safari\/537.36\"","userId":"8"}

## Solution
### Schema Design
The database schema will be modelled following a star schema centered around the 'songplays' table. The star schema has been chosen as a best fit for the type of queries intended.  

Tables:
1. songplays (fact table) - records log data associated with streaming actions for a song
attributes:\
songplay_id   `int` - PK\
start_time    `timestamp`\
user_id       `varchar`\
level         `ENUM(free, paid)`\
song_id       `varchar`\
artist_id     `varchar`\
session_id    `bigint`\
location      `varchar`\
user_agent    `varchar`

2. users (dimension table) - contains the users in the app\
on conflict do nothing - a single row per user provides all the necessary info\
attributes:\
user_id       `varchar` - PK\
first_name    `varchar`\
last_name     `varchar`\
gender        `varchar`\
level         `ENUM(free, paid)`

3. songs (dimension table) - contains the songs in the music database\
on conflict do nothing - a single row per song provides all the necessary info\
attributes:\
song_id       `varchar` - PK\
title         `varchar`\
artist_id     `varchar`\
year          `int`\
duration      `numeric`

4. artists (dimension table) - artists in the music database\
on conflict do nothing - a single row per artist provides all the necessary info\
attributes: \
artist_id     `varchar` - PK\
name          `varchar`\
location      `varchar`\
latitude      `numeric`\
longitude     `numeric`

5. time (dimension table) - timestamps of records in 'songplays' into specific units\
on conflict do nothing - since the timestamp is very precise, we assume there shouldn't be multiple entries with the exact same timestamp\
attributes:\
start_time    `timestamp` - PK\
hour          `int`\
day           `int`\
week          `int`\
month         `int`\
year          `int`\
weekday       `int`

### ETL Pipeline
The etl pipeline is constructed in the steps detailed below:
1. extract and process the song dataset
2. extract and process the log dataset
3. load the new tables with the processed data

### Stack
Jupyter Notebook\
Python\
Psycopg2\
Pandas\
Postgres


