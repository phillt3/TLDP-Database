# DBHandler.py
# Defines the methods to be used to set up and insert into the GameFilter SQL Datbase

import sqlite3
import DTO


class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.cursor.execute(query)
        self.conn.commit()
        
    def create_games_table(self):
        #The games table will consist of 8 columns with the game ID being the primary key (id, slug, game name, metacritic score, date released, rating on 1-5 scale, avg playtime, background_image url)
        games_table_schema = "id INTEGER PRIMARY KEY UNIQUE, slug TEXT NOT NULL, name TEXT NOT NULL, metacritic INTEGER, released TEXT, rating NUMERIC, playtime INTEGER, background_image TEXT"
        games_table_name = "games"
        self.create_table(games_table_name, games_table_schema)
        
    def create_genres_table(self):
        #The genres table consists of 3 columns (Id (game id), genre id, name of the genre)
        genres_table_schema = "id INTEGER, genre_id INTEGER, name TEXT"
        genres_table_name = "genres"
        self.create_table(genres_table_name, genres_table_schema)
        
    def create_platforms_table(self):
        #The platform table consists of 3 columns (Id (game id), platform id, name of the platform)
        platforms_table_schema = "id INTEGER, plat_id INTEGER, name TEXT"
        platforms_table_name = "platforms"
        self.create_table(platforms_table_name, platforms_table_schema)
        
    def create_errors_table(self):
        #Error table will hold any roolback info should they occur
        errors_table_schema = "error TEXT"
        errors_table_name = "errors"
        self.create_table(errors_table_name, errors_table_schema)
        
    def create_GameFilter_tables(self):
        self.create_games_table()
        self.create_genres_table()
        self.create_platforms_table()
        self.create_errors_table()
        
        
    def delete_table(self, table_name):
        query = f"DROP TABLE {table_name}"
        self.cursor.execute(query)
        self.conn.commit()
        
    def close_connection(self):
        self.conn.close()
        
    def perform_batch_transaction(self, games):
        #this method is a contained operation to do a bulk insert of formatted game, genre, and platform records
        try:
            self.cursor.execute("BEGIN")
            
            self.cursor.executemany(f"INSERT INTO games ({DTO.Game.getProps()}) VALUES (?,?,?,?,?,?,?,?)", [game.getValues() for game in games])
            self.cursor.executemany(f"INSERT INTO genres ({DTO.Genre.getProps()}) VALUES (?,?,LOWER(?))", [genre.getValues() for game in games for genre in game.genres])
            self.cursor.executemany(f"INSERT INTO platforms ({DTO.Platform.getProps()}) VALUES (?,?,LOWER(?))", [platform.getValues() for game in games for platform in game.platforms])
            
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            self.cursor.execute(f"INSERT INTO errors (error) VALUES (?)", e)
            self.conn.commit()