import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Description: This function can be used to read the file in the filepath (data/song_data)
    to get the song and artist data and load it into the songs and artists tables.

    Arguments:
        cur: the cursor object. 
        filepath: song data file path. 

    Returns:
        None
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df.head()[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df.head()[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Description: This function can be used to read the file in the filepath (data/log_data) in order
    to get the user and time info and load it into the users, time and songplays tables.

    Arguments:
        cur: the cursor object. 
        filepath: log data file path. 

    Returns:
        None
    """
    # open log file
    df = pd.read_json(filepath, lines=True)
    
    # filter by NextSong action
    df = df[df['page'] == 'NextSong']
    
    # convert timestamp column to datetime
    t = df['ts'] = pd.to_datetime(df['ts'], unit='ms')
        
    # insert time data records
    
    time_data = [t, t.dt.hour, t.dt.day, t.dt.weekofyear, t.dt.month, t.dt.year, t.dt.dayofweek]
    column_labels = ["start_time", "hour", "day", "week of year", "month", "year", "weekday"]
    d = {column_labels[0] : time_data[0], column_labels[1] : time_data[1],\
         column_labels[2] : time_data[2], column_labels[3] : time_data[3],\
         column_labels[4] : time_data[4], column_labels[5] : time_data[5],\
         column_labels[6] : time_data[6], column_labels[6] : time_data[6]}
    time_df = pd.DataFrame(data=d)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = pd.read_json(filepath, lines=True)[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    counter = 0;
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        extracted = df[['ts','userId', 'level', 'sessionId', 'location', 'userAgent']]
        print()
        songplay_data = [extracted.values[counter][0], extracted.values[counter][1], extracted.values[counter][2], songid, artistid,\
                         extracted.values[counter][3], extracted.values[counter][4],\
                         extracted.values[counter][5]]

        counter = counter + 1;
        
        cur.execute(songplay_table_insert, songplay_data)

def process_data(cur, conn, filepath, func):
    """
    Description: This function loads all the json files in the provided path, counts
    the total number of files and applies the provided function to these files.

    Arguments:
        cur: the cursor object. 
        conn: database connection.
        filepath: file path to the files to be loaded.
        func: function to be applied to the files.
        
    Returns:
        None
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()