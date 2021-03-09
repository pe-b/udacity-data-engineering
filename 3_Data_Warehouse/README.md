# Data Warehouse

Data Warehouse project for the third module of the Data Engineering Nanodegree.

## Summary
The project consists of the design and implementation of an etl pipeline between AWS S3 and Redshift. The data is finally modelled into a set of dimensional tables to allow flexible querying.

## Motivation
Practice and apply to a real-world scenario the concepts covered in the 'Data Warehouse' module such as:\
- Dimensional modelling
- ETL with AWS
- AWS IAM, S3 and Redshift
- Infrastructure as code
- Data warehouse design

## Project Details

### Introduction
A music streaming startup, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.
The task consists of building an ETL pipeline that extracts the data from S3, stages it in Redshift, and transforms data into a set of dimensional tables for the analytics team to continue finding insights in what songs their users are listening to.
### Existing Data
The pre-existing data resides in S3 and consists of two datasets:\

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
The new data is modelled using a star schema as follows:\
#### Staging Tables
**staging_events** - table used for staging events\
artist `VARCHAR`,\
auth `VARCHAR`,\
firstName `VARCHAR`,\
gender `VARCHAR`,\
itemInSesssion `VARCHAR`,\
lastName `VARCHAR`,\
length `FLOAT`,\
level `VARCHAR`,\
location `VARCHAR`,\
method `VARCHAR`,\
page `VARCHAR`,\
registration `FLOAT`,\
sessionId `INTEGER`,\
song `VARCHAR`,\
status `INTEGER`,\
ts `TIMESTAMP`,\
userAgent `VARCHAR`,\
userId `INTEGER`

**staging_songs** - table used for staging songs\
num_songs `INTEGER`,\
artist_id `VARCHAR`,\
artist_latitude `FLOAT`,\
artist_longitude `FLOAT`,\
artist_location `VARCHAR`,\
artist_name `VARCHAR`,\
song_id `VARCHAR`,\
title `VARCHAR`,\
duration `FLOAT`,\
year `INTEGER`
#### Fact Table
**songplays** - records in event data associated with song plays i.e. records with page NextSong\
songplay_id `INTEGER` SORTKEY,\
start_time `TIMESTAMP`,\
user_id `INTEGER`,\
level `VARCHAR`,\
song_id `VARCHAR` DISTKEY,\
artist_id `VARCHAR`,\
session_id `INTEGER`,\
location `VARCHAR`,\
user_agent `VARCHAR`

#### Dimension Tables
**users** - users in the app\
user_id `INTEGER` SORTKEY,\
first_name `VARCHAR`,\
last_name `VARCHAR`,\
gender `VARCHAR`,\
level `VARCHAR`

**songs** - songs in music database\
song_id `VARCHAR` SORTKEY,\
title `VARCHAR`,\
artist_id `VARCHAR` DISTKEY,\
year `INTEGER`,\
duration `FLOAT`

**artists** - artists in music database\
artist_id `VARCHAR` SORTKEY,\
name `VARCHAR`,\
location `VARCHAR`,\
lattitude `FLOAT`,\
longitude `FLOAT`

**time** - timestamps of records in songplays broken down into specific units\
start_time `TIMESTAMP` SORTKEY,\
hour `INTEGER`,\
day `INTEGER`,\
week `INTEGER`,\
month `VARCHAR`,\
year `INTEGER`,\
weekday `INTEGER`
### ETL
The etl is implemented through the following files:
1. `sql.queries.py` - the sql queries for dropping, creating and loading the data\
2. `dwh.cfg` - configs for aws infra as code\
3. `create_cluster.py` - creates IAM role and Redshift cluster\
4. `create_tables.py` - creates the staging and final tables\
5. `etl.py` - loads the data into the new tables\
6. `clean_up_resources.py` - deletes the cluster and the role

### Steps Taken towards Solution
1. Modelled final tables with a star schema
2. Scripts for creating the Redshift cluster and IAM role
3. Sql queries for droping, creating and loading the tables
4. Code for creating the tables
5. Etl scripts
6. Scripts for cleaning up the resources

### Tech Stack
Python
AWS
- IAM
- S3
- Redshift
Boto3
Psycopg2
Jupyter
Pandas

### Resources
1. Udacity Data Warehouse with AWS lectures
2. AWS Redshift Docs (https://docs.aws.amazon.com/redshift/?id=docs_gateway)
3. AWS IAM Docs (https://docs.aws.amazon.com/iam/?id=docs_gateway)
4. Boto3 Docs (https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

## How to Run the Project
1. Fill in the following in `dwh.cfg`\
- your aws account details under [AWS] [KEY]/[SECRET]\
- I provided a default configuration (cheapest at the time of writing) for 
the redshift cluster but feel free to change it.
2. Run `create_cluster.py`\
- it may take a few minutes until the cluster becomes 'available'.\
- run multiple times creat_cluster.py as once the cluster is avaialble, the script\
  will return the cluster's endpoint and arn\
- copy the endpoint to `dwh.cfg` under [CLUSTER]/[HOST] and the arn under
[IAM_ROLE]/[ARN]\
3. Run `create_tables.py`\
- the tables will not be created before cluster is active.
4. Run `etl.py`\
- this will take a few minutes depending on what AWS configuratio you chose.\
5. Once step 4 is complete, you have your data ready to be queried in Redshift.
6. When done, run clean_up_resources.py to delete the cluster and the role created at step 1.\
- run this multiple times until you receive 'Cluster not found' to make sure you deleted it.

Find project repository at [Project link](https://github.com/pe-b/udacity-data-engineering/tree/main/3_Data_Warehouse).