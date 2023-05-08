class StreamLocations():
    def set_streaming_locations(self, stream_dict: dict) -> None:   
        if stream_dict['streamingInfo']:
            streaming_info = stream_dict['streamingInfo']['gb']
            services = [keys for keys in streaming_info.keys()]
            self.streaming_locations = {}
            for service in services:
                self.streaming_locations[service] = streaming_info[service][0]['link']
        else:
            self.streaming_locations = False        
        

class Show():
    def __init__(self, show_dict: dict) -> None:
        self.title = show_dict['title']
        self.overview = show_dict['overview']
        self.imdb_rating = show_dict['imdbRating']
        if list(show_dict['posterURLs'].values()):
            self.poster = show_dict['posterURLs']['780']
        else:
            self.poster = False
        

class Movie(Show, StreamLocations):
    def __init__(self, movie_dict: dict) -> None:
        super().__init__(movie_dict)
        self.set_streaming_locations(movie_dict)
    
    def get_show_information(self) -> dict:
        return {"title": self.title, 
                "poster": self.poster, 
                "streams": self.streaming_locations}


class Series(Show):
    def __init__(self, series_dict: dict) -> None:
        super().__init__(series_dict)
        
        self.seasons_streaming_info = self.set_seasons_streaming_info(series_dict['seasons'])           

    def set_seasons_streaming_info(self, seasons_list: list) -> list:
        return [Season(season) for season in seasons_list]
    
    def get_show_information(self) -> list:
        show_info = []
        for season in self.seasons_streaming_info:
            show_info.append({"title": f'{self.title} {season.season}',
                              "poster": self.poster,
                              "streams": season.streaming_locations})
        return show_info


class Season(StreamLocations):
    def __init__(self, season_dict: dict) -> None:
        self.season = season_dict['title']
        self.set_streaming_locations(season_dict)

    

