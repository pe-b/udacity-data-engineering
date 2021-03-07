import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')
IAM_ROLE = config['IAM_ROLE']['ARN']
LOG_DATA = config['S3']['LOG_DATA']
LOG_JSONPATH = config['S3']['LOG_JSONPATH']
SONG_DATA = config['S3']['SONG_DATA']

# DROP TABLES
staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES
staging_events_table_create= ("""CREATE TABLE staging_events 
(
    artist            VARCHAR,
    auth              VARCHAR,
    first_name        VARCHAR,
    gender            VARCHAR,
    item_in_session   INTEGER,
    last_name         VARCHAR,
    length            DECIMAL,
    level             VARCHAR,
    location          VARCHAR,
    method            VARCHAR,
    page              VARCHAR,
    registration      DECIMAL,
    session_id        INTEGER,
    song              VARCHAR,
    status            INTEGER,
    time_stamp        BIGINT,
    user_agent        VARCHAR,
    user_id           INTEGER    
);
""")

staging_songs_table_create = ("""CREATE TABLE staging_songs
(
    num_songs          INTEGER,
    artist_id          VARCHAR,
    artist_latitude    DECIMAL,
    artist_longitude   DECIMAL,
    artist_location    VARCHAR,
    artist_name        VARCHAR,
    song_id            VARCHAR,
    title              VARCHAR,
    duration           DECIMAL,
    year               INTEGER
);
""")

songplay_table_create = ("""CREATE TABLE songplays
(
    songplay_id        INTEGER       IDENTITY(0,1)    SORTKEY,
    start_time         TIMESTAMP,
    user_id            INTEGER,
    level              VARCHAR,
    song_id            INTEGER       DISTKEY,
    artist_id          INTEGER,
    session_id         INTEGER,
    location           VARCHAR,
    user_agent         VARCHAR
);
""")

user_table_create = ("""CREATE TABLE users
(
    user_id        INTEGER    NOT NULL    SORTKEY,
    first_name     VARCHAR    NOT NULL,
    last_name      VARCHAR    NOT NULL,
    gender         VARCHAR,
    level          VARCHAR    NOT NULL 
);
""")

song_table_create = ("""CREATE TABLE songs
(
    song_id        INTEGER    NOT NULL    SORTKEY,
    title          VARCHAR    NOT NULL,
    artist_id      INTEGER    NOT NULL    DISTKEY,
    year           INTEGER,
    duration       DECIMAL
);
""")

artist_table_create = ("""CREATE TABLE artists
(
    artist_id        INTEGER    NOT NULL    SORTKEY,
    name             VARCHAR    NOT NULL,
    location         VARCHAR,
    latitude         DECIMAL,
    longitude        DECIMAL
);
""")

time_table_create = ("""CREATE TABLE time
(
    start_time    TIMESTAMP  NOT NULL    SORTKEY,
    hour          INTEGER    NOT NULL,
    day           INTEGER    NOT NULL,
    week          INTEGER    NOT NULL,
    month         VARCHAR    NOT NULL,
    year          INTEGER    NOT NULL,
    weekday       VARCHAR    NOT NULL
);
""")

# STAGING TABLES
staging_events_copy = ("""
    copy staging_events FROM {}
    credentials 'aws_iam_role={}'
    region 'us-west-2'
    format as json {};
""").format(LOG_DATA, IAM_ROLE, LOG_JSONPATH)

staging_songs_copy = ("""
    copy staging_songs FROM {}
    credentials 'aws_iam_role={}'
    region 'us-west-2'
    json 'auto'
""").format(SONG_DATA, IAM_ROLE)

# FINAL TABLES
songplay_table_insert = ("""
    insert into songplays
    values(%s, %s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
    insert into users
    values(%s, %s, %s, %s, %s)
""")

song_table_insert = ("""
    insert into songs
    values(%s, %s, %s, %s, %s)
""")

artist_table_insert = ("""
    insert into artists
    values(%s, %s, %s, %s, %s)
""")

time_table_insert = ("""
    insert into time
    values(%s, %s, %s, %s, %s, %s, %s)
""")

# QUERY LISTS
create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
