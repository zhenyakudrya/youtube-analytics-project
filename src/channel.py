import json
import os
from googleapiclient.discovery import build
import isodate


class Channel:
    """Класс для ютуб-канала"""

    youtube = build('youtube', 'v3', developerKey=os.getenv('YT_API_KEY'))

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API."""
        self.channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.id_channel = self.channel["items"][0]['id']
        self.title = self.channel["items"][0]["snippet"]['title']
        self.channel_description = self.channel["items"][0]["snippet"]["description"]
        self.url = self.channel["items"][0]["snippet"]["thumbnails"]["default"]["url"]
        self.subscribers_count = self.channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self.channel["items"][0]["statistics"]["videoCount"]
        self.quantity_views = self.channel["items"][0]["statistics"]["viewCount"]

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        return self.channel_id == channel_id

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        return cls.youtube

    def to_json(self, file_name):
        """ Cоздаем файл 'moscowpython.json' в данными по каналу """
        data = {
            "channel_id": self.channel["items"][0]['id'],
            "title": self.channel["items"][0]["snippet"]['title'],
            "channel_description": self.channel["items"][0]["snippet"]["description"],
            "url": self.channel["items"][0]["snippet"]["thumbnails"]["default"]["url"],
            "subscribers_count": self.channel["items"][0]["statistics"]["subscriberCount"],
            "video_count": self.channel["items"][0]["statistics"]["videoCount"],
            "quantity_views": self.channel["items"][0]["statistics"]["viewCount"]
        }
        with open("moscowpython.json", "w") as json_file:
            json.dump(data, json_file)

