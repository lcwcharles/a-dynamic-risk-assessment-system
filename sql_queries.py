# DROP TABLES

finaldata_table_drop = "DROP TABLE IF EXISTS finaldata;"
ingestedfiles_table_drop = "DROP TABLE IF EXISTS ingestedfiles;"
latestscore_table_drop = "DROP TABLE IF EXISTS latestscore;"
apireturns_table_drop = "DROP TABLE IF EXISTS apireturns;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

finaldata_table_create = """
                        CREATE TABLE IF NOT EXISTS finaldata 
                            (
                                data_id serial PRIMARY KEY, 
                                corporation VARCHAR NOT NULL,
                                lastmonth_activity INT NOT NULL,
                                lastyear_activity INT NOT NULL,
                                number_of_employees INT NOT NULL,
                                exited BOOLEAN NOT NULL
                            );
                        """

ingestedfiles_table_create = """
                    CREATE TABLE IF NOT EXISTS ingestedfiles 
                        (
                            file_id serial PRIMARY KEY,  
                            file_name VARCHAR NOT NULL
                        );
                    """

latestscore_table_create = """
                    CREATE TABLE IF NOT EXISTS latestscore 
                        (
                            latestscore VARCHAR PRIMARY KEY
                        );
                    """

apireturns_table_create = """
                        CREATE TABLE IF NOT EXISTS apireturns 
                            (
                                api_id serial PRIMARY KEY,  
                                predictions VARCHAR NOT NULL, 
                                score VARCHAR NOT NULL，
                                lastmonth_activity_summary VARCHAR NOT NULL,
                                lastyear_activity_summary VARCHAR NOT NULL,
                                number_of_employees_summary VARCHAR NOT NULL,
                                ingestion_time VARCHAR NOT NULL,
                                training_time VARCHAR NOT NULL,
                                missing_data VARCHAR NOT NULL,
                                outdated_packages_list VARCHAR NOT NULL
                            );
                      """

time_table_create = """
                    CREATE TABLE IF NOT EXISTS time 
                        (
                            start_time TIMESTAMP PRIMARY KEY,  
                            hour INT NOT NULL, 
                            day INT NOT NULL, 
                            week INT NOT NULL, 
                            month INT NOT NULL, 
                            year INT NOT NULL,  
                            weekday INT NOT NULL
                        );
                    """

# INSERT RECORDS

finaldata_table_create = """
                        INSERT INTO finaldata 
                            (
                                data_id, 
                                corporation,
                                lastmonth_activity,
                                lastyear_activity,
                                number_of_employees,
                                exited
                            ) 
                            VALUES (%s, %s, %s, %s, %s, %s);
                        """

ingestedfiles_table_create = """
                    INSERT INTO ingestedfiles 
                        (
                            file_id,  
                            file_name
                        ) 
                        VALUES (%s, %s);
                    """

latestscore_table_create = """
                      INSERT INTO latestscore 
                          (
                              latestscore
                          ) 
                          VALUES (%s);
                      """

apireturns_table_create = """
                    INSERT INTO apireturns 
                        (
                            api_id,  
                            predictions, 
                            score,
                            lastmonth_activity_summary,
                            lastyear_activity_summary,
                            number_of_employees_summary,
                            ingestion_time,
                            training_time,
                            missing_data,
                            outdated_packages_list
                        ) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s;
                    """

time_table_insert = """
                    INSERT INTO time 
                        (
                            start_time, 
                            hour,
                            day, 
                            week, 
                            month, 
                            year, 
                            weekday
                        ) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (start_time) 
                        DO NOTHING;
                    """

# FIND SONGS
# Implement the song_select query in sql_queries.py to find the song ID and artist ID based on the title, artist name, and duration of a song.
# song_select, (row.song, row.artist, row.length)
song_select = """
                SELECT song_id, songs.artist_id 
                FROM songs 
                JOIN artists ON songs.artist_id = artists.artist_id 
                WHERE songs.title=%s AND artists.name=%s AND songs.duration=%s;
              """

# QUERY LISTS

create_table_queries = [finaldata_table_create, ingestedfiles_table_create, 
                        latestscore_table_create, apireturns_table_create]
drop_table_queries = [finaldata_table_drop, ingestedfiles_table_drop, 
                        latestscore_table_drop, apireturns_table_drop]