# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import youtube_dl
import db
import config
from time import sleep


def get_items(playlist):
    options = {}
    options['extract_flat'] = 'in_playlist'
    with youtube_dl.YoutubeDL(options) as ydl:
        playlist_info = ydl.extract_info(playlist, download=False)
    print len(playlist_info['entries'])
    for entry in playlist_info['entries']:
        if entry['title'] == '[Deleted video]':
            playlist_info['entries'].remove(entry)
    return playlist_info


def download_video(yid):
    info = {}
    info['yid'] = yid
    options = {}
    options['format'] = 'bestaudio/best'
    options['extractaudio'] = True
    options['postprocessors'] = [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]

    info_dict = {}
    info_dict['upload_date'] = None
    while info_dict['upload_date'] is None:
        print 'Trying to grab information for video...'
        with youtube_dl.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(yid, download=False)
        sleep(1)

    info['title'] = info_dict['title'].replace('/', '／')
    info['pubDate'] = info_dict['upload_date']
    info['description'] = info_dict['description']
    my_id = db.add_video(info)
    filename = str(my_id) + '. ' + info['title'] + '.mp3'
    full_path = config.get_path('mp3', filename)
    options['outtmpl'] = full_path

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([config.get_option('YOUTUBE_VIDEO_BASE_URL') + yid])
    return info


def get_missing_episodes():
    playlist = config.get_option('PLAYLIST_URL')
    published_videos = get_items(playlist)['entries']
    downloaded_videos = db.get_downloaded_videos(1)
    for video in published_videos:
        yid = video['id']
        if yid not in downloaded_videos:
            print "Downloading " + yid
            dest = download_video(yid)
