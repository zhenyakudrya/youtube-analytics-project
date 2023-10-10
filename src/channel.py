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
        self.__channel_id = channel_id
        self._init_from_api

    def __str__(self):
        return f'{self.title} ({self.url})'

    @property
    def _init_from_api(self):

        channel = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        self.title = channel['items'][0]['snippet']['title']

        self.description = channel['items'][0]['snippet']['description']

        self.url = f'https://www.youtube.com/channel/{channel["items"][0]["id"]}'

        self.subscriber_count = channel['items'][0]['statistics']['subscriberCount']

        self.video_count = channel['items'][0]['statistics']['videoCount']

        self.view_count = channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        return self.__channel_id

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

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __sub__(self, other):
        return int(other.subscriber_count) - int(self.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other):
        return int(self.subscriber_count) == int(other.subscriber_count)
