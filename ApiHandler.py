# ApiHandler.py
# Responsible for RAWG API GET request and paging through response

import config
import requests
import DTO
import DBHandler
    
# This method is responsible for fetching and paging through the list of games received by the RAWG API and then calling the db manager to handle insertion
# NOTE: This method could potentially benefit in future versions from async implementation
def fetch_games(batch_size, transaction_num):
    
    params = {
        'key': config.RAWG_API_KEY,
        'ordering': '-metacritic', #due to current 4000 limit with RAWG data GET, prioritize highest ranked games
        'page_size': batch_size #set page size to batch size so that transactions are not split between pages of data
    }
    
    db_manager = DBHandler.DatabaseManager(config.GAMEFILTER_DB_PATH)
    db_manager.create_GameFilter_tables()
    
    try:
        next_url = config.RAWG_API_BASE_URL
        
        for x in range(transaction_num): #will only process as many pages of data as set by transaction_num
            response = requests.get(next_url, params) if x == 0 else requests.get(next_url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()
            game_DTOs = [DTO.Game(game.get('id'), game.get('slug'), game.get('name'), game.get('metacritic'), game.get('released'), game.get('rating'), game.get('playtime'), game.get('background_image'), game.get('genres'), game.get('platforms')) for game in data.get('results', [])]
            db_manager.perform_batch_transaction(game_DTOs)
            
            next_url = data.get("next")
            if not next_url:
                break
            
    except requests.exceptions.RequestException as e:
        #Log error that occurs while handling API request
        print(f"Error: {e}")
    
    db_manager.close_connection()
        
