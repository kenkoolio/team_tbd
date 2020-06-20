# download videos from URLS

from pytube import YouTube

import os
import shutil

test_url = 'https://www.youtube.com/watch?v=FApbkER3uIY'
ILLEGAL = ['?', ':', '*', '>', '<', "'", '"', '#', '%', '&', '{', '}', "\\", '/', "$", '!', '@', '+', "`", '|', "=" ]

def clean_title(title):
    title = list(title) #use list to split string on characters
    output = []
    for character in title:
        print(character)
        if character == ' ':
            output.append('-')
        elif character not in ILLEGAL:
            output.append(character)
    return "".join(output)


def download_video(video_url, output_dir):
    if 'youtube.com' in video_url:
        return download_youtube(video_url, output_dir)
    elif 'oregonstate.edu' in video_url:
        pass
    return None


def download_youtube(video_url, output_dir):
    try:
        video = YouTube(video_url)
        title = video.title
        title = clean_title(title)

        streams = video.streams.filter(file_extension="mp4")
        itag = streams[0].itag
        extension = streams[0].mime_type.split('/')[1]

        # file_directory = os.path.join(output_dir, title)
        video.streams.get_by_itag(itag).download(output_path=output_dir, filename=title)
        return title + '.' + extension
    except Exception as e:
        print(f'ERROR in download_youtube: {e}')
        raise


