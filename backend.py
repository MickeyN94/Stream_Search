import requests
import base64
from pathlib import Path
from models import Movie, Series
import constants

def get_shows(search_title: str) -> list[dict[str, str | dict]]:
    url = "https://streaming-availability.p.rapidapi.com/v2/search/title"

    headers = {
	"X-RapidAPI-Key": constants.API_KEY,
	"X-RapidAPI-Host": "streaming-availability.p.rapidapi.com"
}

    querystring = {"title":search_title,"country":"gb","output_language":"en", "show_type": "all"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    
    titles = response.json()['result']
    shows = [] 
    for title in titles:
        if title['type'] == 'movie':
            movie = Movie(title)
            shows.append(movie.get_show_information())
        elif title['type'] == 'series':
            series = Series(title)
            all_seasons = series.get_show_information()
            for season in all_seasons:
                shows.append(season)
    return shows
            
        
def get_service_logo(service :str) -> str:
    # get the file location of the logo
    
    path = Path(__file__).parent / 'images'
    code2 = (path / f'{service}.webp').read_bytes()
    return f"data:image/webp;base64,{base64.b64encode(code2).decode()}"    



def get_tvshows(search_title: str) -> list[Movie]:
    url = "https://streaming-availability.p.rapidapi.com/v2/search/title"

    headers = {
	"X-RapidAPI-Key": "8979319a71msh9488a4fb18dd72fp15c167jsn5bfb9ed47813",
	"X-RapidAPI-Host": "streaming-availability.p.rapidapi.com"
}

    querystring = {"title":search_title,"country":"gb","output_language":"en", "show_type": "series"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    
    titles = response.json()['result']
    return [Series(title) for title in titles if title['type'] == 'series']


