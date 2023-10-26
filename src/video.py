from googleapiclient.discovery import build
import os
from src.channel import APIMixin


class Video(APIMixin):

    youtube = APIMixin.get_service()

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        self._init_from_api

    def __str__(self):
        return f'{self.title}'

    @property
    def _init_from_api(self):
        try:
            video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                        id=self.video_id).execute()
            self.id_video = video_response["items"][0]["id"]
            self.title = video_response['items'][0]['snippet']['title']
            self.url = f'https://youtu.be/{self.id_video}'
            self.view_count = video_response['items'][0]['statistics']['viewCount']
            self.like_count = video_response['items'][0]['statistics']['likeCount']
        except IndexError:
            video_response = None
            self.id_video = None
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id


