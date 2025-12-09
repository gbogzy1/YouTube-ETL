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



def extract_video_data(video_ids):

    extracted_data = []

    def batch_list(video_id_lst,batch_size):
        for video_id in range(0, len(video_id_lst), batch_size):
            yield video_id_lst[video_id : video_id + batch_size]

    

    try:
        for batch in batch_list(video_ids, max_results):
            video_ids_str = ",".join(batch)

            url = f'https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}'
            
            response = requests.get(url)

            response.raise_for_status()

            data = response.json()

            for item in data.get('items',[]):
                video_id = item['id']
                snippet = item['snippet']
                contentDetails = item['contentDetails']
                statistics = item['statistics']
            
            video_data = {
                "video_id" : video_id,
                "title" : snippet['title'],
                "publishedAt" : snippet['publishedAt'],
                "duration" : contentDetails['duration'],
                "viewcount" : statistics.get("viwecount", None),
                "likecount" : statistics.get("likecount", None),
                "commentcount" : statistics.get("commentcount", None)
            }

            extracted_data.append(video_data)


        return extracted_data
    
    except requests.exceptions.RequestException as e:
        raise e




if __name__ == "__main__":
    playlist_id = get_playlist_id(Channel_Handle)
    video_ids = get_video_id(playlist_id)
    print(extract_video_data(video_ids))
