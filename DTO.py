# Game.py
# Defines classes that can be used to represent Data Transfer Objects for the API -> DB process

#Each game JSON object has genre sub object, this class extracts and formats it
class Genre:
    def __repr__(self):
        return f"(id: {self.id}, genre_id: {self.genre_id}, name: {self.name})"
    
    @staticmethod
    def getProps():
        return "id, genre_id, name"
        
    def getValues(self):
        return (self.id, self.genre_id, self.name)
    
    def __init__(self, id, genre_id, name):
        self.id = id #int game id
        self.genre_id = genre_id #int value to mark genre, not the game id
        self.name = name #string name of genre

#Each game JSON object has platform sub object, this class extracts and formats it     
class Platform:
    def __repr__(self):
        return f"(id: {self.id}, plat_id: {self.genre_id}, name: {self.name})"
    
    @staticmethod
    def getProps():
        return "id, plat_id, name"
        
    def getValues(self):
        return (self.id, self.plat_id, self.name)
    
    def __init__(self, id, plat_id, name):
        self.id = id #int game id
        self.plat_id = plat_id #int value to mark platform, not the game id
        self.name = name #string name of platform

#Extracts and formats individiual JSON game object from API request result property
class Game:
    @staticmethod
    def getGenreList(genres, game_id):
        if not genres:
            return []
        
        genre_list = [Genre(game_id, genre.get('id'), genre.get('name')) for genre in genres]

        return genre_list
    
    @staticmethod
    def getPlatformList(platforms, game_id):
        if not platforms:
            return []
        
        platform_list = [Platform(game_id, platform_obj.get('platform').get('id'), platform_obj.get('platform').get('name')) for platform_obj in platforms]
            
        return platform_list
    
    @staticmethod
    def getProps():
        return "id, slug, name, metacritic, released, rating, playtime, description, background_image"
        
    def getValues(self):
        return (self.id, self.slug, self.name, self.metacritic, self.released, self.rating, self.playtime, self.description, self.background_image)
        
    def __repr__(self):
        return f"(id: {self.id}, slug: {self.slug}, name: {self.name}, metacritic: {self.metacritic}, released: {self.released}, rating: {self.rating}, playtime: {self.playtime}, description: {self.description}, background_image: {self.background_image}, genres: {self.genres}, platforms: {self.platforms})"
    
    def __init__(self,id, slug, name, metacritic, released, rating, playtime, description, background_image, genres, platforms):
        self.id = id #int UUID for game
        self.slug = slug #string formatted title of game to be all lowercase and have -'s
        self.name = name #string title of game
        self.metacritic = metacritic #int 1-100 for metacritic score
        self.released = released #string date of release
        self.rating = rating #double rating out of 5
        self.playtime = playtime #int average steam playtime hours
        self.description = description #description of game
        self.background_image = background_image #string url to image
        self.genres = Game.getGenreList(genres, id) #an array of genre objects
        self.platforms = Game.getPlatformList(platforms, id) #an array of platform objects