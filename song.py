import discord
from youtube_dl import YoutubeDL

from youtube_search import YoutubeSearch

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'False'}


class Song(object):
    playing = False

    def __init__(self, meta, text_channel, voice_channel, client, author, avatar):
        try:
            res = YoutubeSearch(meta, max_results=1).to_dict()
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(res[0]['id'], download=False)
                self.track = info['formats'][0]['url']
                self.title = info['title']
                self.image_url = info['thumbnails'][0]['url']
                self.video_url = info['webpage_url']
        except Exception as e:
            print(e)

        self.text_channel = text_channel
        self.voice_channel = voice_channel
        self.client = client
        self.author = author
        self.avatar = None if avatar is None else avatar.url

    def create_message(self, type_, index):
        if type_ == 'playing':
            embed = discord.Embed(title=':musical_note: Now playing', description=f'[{self.title}]({self.video_url})',
                                  color=discord.Color.blue())
            embed.set_thumbnail(url=self.image_url)
            embed.set_footer(text=f'Added by {self.author}', icon_url=self.avatar)
            return embed

        elif type_ == 'add_to_queue':
            embed = discord.Embed(title=f'Position in queue #{index}',
                                  description=f'[{self.title}]({self.video_url})', color=discord.Color.blue())
            embed.set_thumbnail(url=self.image_url)
            embed.set_footer(text=f'Added by {self.author}', icon_url=self.avatar)
            return embed
