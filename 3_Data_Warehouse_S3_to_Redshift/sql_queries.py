import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')
IAM_ROLE = config['IAM_ROLE']['ARN']
LOG_DATA = config['S3']['LOG_DATA']
LOG_JSONPATH = config['S3']['LOG_JSONPATH']
SONG_DATA = config['S3']['SONG_DATA']

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS events"
staging_songs_table_drop = "DROP TABLE IF EXISTS songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE events 
(
    key               integer(0,1)    not null,
    artist            varchar(25)     not null,
    auth              varchar(15)     not null,
    first_name        varchar(15),
    gender            varchar(3),
    item_in_session   integer         not null,
    last_name         varchar(15),
    length            decimal,
    level             varchar(4),
    location          varchar(30),
    method            varchar(6),
    page              varchar(12),
    registration      decimal,
    session_id        integer,
    song              varchar(30),
    status            integer,
    time_stamp        bigint,
    user_agent        varchar(30),
    user_id           integer    
);
""")

staging_songs_table_create = ("""CREATE TABLE songs
(
    num_songs          integer        not null,
    artist_id          varchar(20)    not null,
    artist_latitude    decimal,
    artist_longitude   decimal,
    artist_location    varchar(20),
    artist_name        varchar(20),
    song_id            varchar(20),
    title              varchar(20),
    duration           decimal,
    year               integer
);
""")

songplay_table_create = ("""CREATE TABLE songplays
(
    songplay_id        identity(0,1)    not null,
    start_time         timestamp,
    user_id            integer,
    level              varchar(4),
    song_id            integer,
    artist_id          integer,
    session_id         integer,
    location           varchar(30),
    user_agent         varchar(30)
);
""")

user_table_create = ("""CREATE TABLE users
(
    user_id        integer        not null,
    first_name     varchar(10)    not null,
    last_name      varchar(10)    not null,
    gender         varchar(3),
    level          varchar(10)    not null
);
""")

song_table_create = ("""CREATE TABLE songs
(
    song_id        integer        not null,
    title          varchar(30)    not null,
    artist_id      integer        not null,
    year           integer,
    duration       decimal
);
""")

artist_table_create = ("""CREATE TABLE artists
(
    artist_id        integer        not null,
    name             varchar(30)    not null,
    location         varchar(30),
    latitude         decimal,
    longitude        decimal
);
""")

time_table_create = ("""CREATE TABLE time
(
    start_time    timestamp    not null,
    hour          integer      not null,
    day           integer      not null,
    week          integer      not null,
    month         varchar(10)  not null,
    year          integer      not null,
    weekday       varchar(10)  not null
);
""")

# STAGING TABLES

staging_events_copy = ("""
    copy staging_events FROM {}
    credentials 'aws_iam_role={}'
    region 'us-west-2'
    format as json {};
""").format(LOG_DATA,IAM_ROLE,LOG_JSONPATH)

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
