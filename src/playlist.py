from googleapiclient.discovery import build
import os
import isodate
from datetime import timedelta


class PlayList:
    youtube = build('youtube', 'v3', developerKey=os.getenv('YT_API_KEY'))

    def __init__(self, playlist_id):
        playlist_info = self.youtube.playlists().list(id=playlist_id, part='snippet', ).execute()
        self.playlist_id = playlist_id
        self.title = playlist_info['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={playlist_id}'

    def __str__(self):
        return f'{self.total_duration}'

    @property
    def total_duration(self):
        """
        Возвращает объект класса `datetime.timedelta`
        с суммарной длительностью плейлиста
        """
        total_duration = timedelta()
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()

        max_like_count = 0
        url = None
        for video in video_response['items']:
            if int(video['statistics']['likeCount']) > max_like_count:
                url = f'https://youtu.be/{video["id"]}'
        return url
