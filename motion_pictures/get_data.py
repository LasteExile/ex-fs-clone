import json
import requests
import os

months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
          'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}


def get_data(imdb_url, OMDB_API=os.environ.get('OMDB_API'), VIDEOCDN_API=os.environ.get('VIDEOCDN_API')):

    data = {}
    try:
        imdb_id = imdb_url[imdb_url.index('title/')+6:]
        imdb_id = imdb_id[:imdb_id.index('/')]
        data['id'] = imdb_id
    except:
        return False, 'Link is incorrect'
    videocdn_response = requests.get(f'https://videocdn.tv/api/short/?imdb_id={imdb_id}&api_token={VIDEOCDN_API}')
    omdb_response = requests.get(f'http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API}&plot=full')
    videocdn_json = json.loads(videocdn_response.text)
    omdb_json = json.loads(omdb_response.text)

    if videocdn_json.get('data'):
        for i in videocdn_json.get('data'):
            data['iframe_src'] = i.get('iframe_src')
    else:
        return False, 'No videocdn data. Check your link'

    if omdb_json.get('Response') == 'True':
        data['title'] = omdb_json.get('Title')
        data['type'] = omdb_json.get('Type')
        released = omdb_json.get('Released').split()
        data['released'] = f'{released[2]}-{months.get(released[1])}-{released[0]}'
        data['actors'] = omdb_json.get('Actors').split(', ')
        data['directors'] = omdb_json.get('Director').split(', ')
        data['writers'] = omdb_json.get('Writer').split(', ')
        data['plot'] = omdb_json.get('Plot')
        data['languages'] = omdb_json.get('Language').split(', ')
        data['poster'] = omdb_json.get('Poster')
        data['genres'] = omdb_json.get('Genre').split(', ')
        ratings = []
        for i in omdb_json.get('Ratings'):
            ratings.append({'source': i.get("Source"), 'value': i.get("Value")})
        data['ratings'] = ratings
    else:
        return False, 'No OMDB data. Check your link'
    return True, data
