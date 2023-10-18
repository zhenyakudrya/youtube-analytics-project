from googleapiclient.discovery import build
import os


class Video:

    youtube = build('youtube', 'v3', developerKey=os.getenv('YT_API_KEY'))

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        self._init_from_api

    def __str__(self):
        return f'{self.video_title}'

    @property
    def _init_from_api(self):
        video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                    id=self.video_id).execute()
        self.id_video = video_response["items"][0]["id"]
        self.video_title = video_response['items'][0]['snippet']['title']
        self.url = f'https://youtu.be/{self.id_video}'
        self.view_count = video_response['items'][0]['statistics']['viewCount']
        self.like_count = video_response['items'][0]['statistics']['likeCount']


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id


