from tkinter import N
from unicodedata import bidirectional
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('Youtube_API_Key')
Channel_Handle = 'MrBeast'
max_results = 50

def get_playlist_id(Channel_Handle):
    try:   
        url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={Channel_Handle}&key={API_KEY}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        channel_items = data['items'][0]
        playlist_id = channel_items['contentDetails']['relatedPlaylists']['uploads']
        print(playlist_id)
        return playlist_id
        
    except requests.exceptions.RequestException as e:
        raise e

def get_video_id(playlist_id):
    if max_results > 0:
        video_ids = []

        page_token = None

        base_url = f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlist_id}&key={API_KEY}'
        try:
            while True:
                url  = base_url
                if page_token:
                    url += f'&pageToken={page_token}'

                response = requests.get(url)

                response.raise_for_status()

                data = response.json()

                for item in data.get('items',[]):
                    video_id = item['contentDetails']['videoId']
                    video_ids.append(video_id)
                
                page_token = data.get('nextPageToken')
                
                if not page_token:
                    break

            return video_ids

        except requests.exceptions.RequestException as e:
            raise e
    else:
        print("No playlist found")


if __name__ == "__main__":
    playlist_id = get_playlist_id(Channel_Handle)
    get_video_id(playlist_id)
