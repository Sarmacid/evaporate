# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import youtube_dl
import db
import config
from time import sleep
import os
import sys
import urlparse


def get_items(playlist_yid):
    options = {}
    options['extract_flat'] = 'in_playlist'
    with youtube_dl.YoutubeDL(options) as ydl:
        playlist_info = ydl.extract_info(playlist_yid, download=False)
    for entry in playlist_info['entries']:
        if entry['title'] == '[Deleted video]':
            playlist_info['entries'].remove(entry)
    return playlist_info


def add_playlist(playlist_url):
    # Takes a playlist URL, grabs additional information an adds them to the db.
    querystring = urlparse.urlparse(playlist_url).query
    playlist_yid = urlparse.parse_qs(querystring)['list'][0]
    try:
        playlist_yt__info = get_items(playlist_yid)
        db.add_playlist(playlist_yt__info)
    except youtube_dl.utils.DownloadError:
        print "Could not fetch info for that URL, are you sure it's correct?"
        sys.exit()


def download_video(yid, playlist, episode_number):
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

    info['playlist_id'] = playlist['id']
    info['title'] = info_dict['title'].replace('/', '／')
    info['pubDate'] = info_dict['upload_date']
    info['description'] = info_dict['description']
    info['episode_number'] = episode_number
    info['filename'] = str(episode_number) + '. ' + info['title'] + '.mp3'

    db.add_video(info)

    full_path = config.get_path('mp3', playlist['title'])
    full_path = os.path.join(full_path, info['filename'])
    options['outtmpl'] = full_path

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([config.get_option('YOUTUBE_VIDEO_BASE_URL') + yid])
    return info


def get_missing_episodes():
    playlists = db.get_all_playlists()
    for playlist in playlists:
        process_playlist(playlist)


def process_playlist(playlist):
    playlist_yt__info = get_items(playlist['yid'])
    published_videos = playlist_yt__info['entries']
    downloaded_videos = db.get_downloaded_videos(1, playlist['id'])
    for episode_number in range(len(published_videos)):
    #for video in published_videos:
        #yid = video['id']
        yid = published_videos[episode_number]['id']
        if yid not in downloaded_videos:
            download_video(yid, playlist, episode_number + 1)
