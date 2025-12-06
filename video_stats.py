import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('Youtube_API_Key')
Channel_Handle = 'MrBeast'

def get_playlist_id(Channel_Handle):
    try:   
        url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={Channel_Handle}&key={API_KEY}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        channel_items = data['items'][0]
        channel_uploads = channel_items['contentDetails']['relatedPlaylists']['uploads']
        print(channel_uploads)
        return channel_uploads
        
    except requests.exceptions.RequestException as e:
        raise e


if __name__ == "__main__":
    get_playlist_id(Channel_Handle)