# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# DROP ENUMS

level_type_enum_drop = "DROP TYPE IF EXISTS level_type"
gender_type_enum_drop = "DROP TYPE IF EXISTS gender_type"
weekday_type_enum_drop = "DROP TYPE IF EXISTS weekday_type"

# CREATE ENUMS

level_type_enum_create = ("CREATE TYPE level_type AS ENUM ('free', 'paid')")
gender_type_enum_create = ("CREATE TYPE gender_type AS ENUM ('F', 'M', 'Other', 'NA')")
weekday_type_enum_create = ("CREATE TYPE weekday_type AS ENUM ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')")

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays (
                                songplay_id SERIAL PRIMARY KEY,
                                start_time int NOT NULL,
                                user_id int NOT NULL,
                                level level_type,
                                song_id varchar,
                                artist_id varchar,
                                session_id int,
                                location int,
                                user_agent varchar)""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users(
                            user_id int NOT NULL,
                            first_name varchar,
                            last_name varchar,
                            gender gender_type,
                            level level_type)""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs(
                            song_id varchar,
                            title varchar,
                            artist_id varchar,
                            year int,
                            duration numeric)""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists(
                            artist_id varchar,
                            name varchar,
                            location varchar,
                            latitude numeric,
                            longitude numeric)""")
    
time_table_create = ("""CREATE TABLE IF NOT EXISTS time(
                            start_time int,
                            hour int,
                            day int,
                            week int, 
                            month int, 
                            year int, 
                            weekday weekday_type)""")

# INSERT RECORDS

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")


time_table_insert = ("""
""")

# FIND SONGS

song_select = ("""
""")

# QUERY LISTS

drop_enum_queries = [level_type_enum_drop, gender_type_enum_drop, weekday_type_enum_drop]
create_enum_queries = [level_type_enum_create, gender_type_enum_create, weekday_type_enum_create]
create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]