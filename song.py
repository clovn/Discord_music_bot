from youtube_dl import YoutubeDL
from youtube_search import YoutubeSearch

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'False'}

def searcher(meta):
    res = YoutubeSearch(meta, max_results=1).to_dict()
    try:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(res[0]['id'], download=False)
            audio_url = info['formats'][0]['url']
            title = info['title']
            chanel_url = info['channel_url']
            image_url = info['thumbnails'][0]['url']
            video_url = info['webpage_url']

    except:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(res[0]['id'], download=False)
            audio_url = info['formats'][0]['url']
            title = info['title']
            chanel_url = info['channel_url']
            image_url = info['thumbnails'][0]['url']
            video_url = info['webpage_url']
    return [audio_url, title, image_url, video_url]

def update_audio_url(res):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(res, download=False)
        audio_url = info['formats'][0]['url']
        return audio_url

