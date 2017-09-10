import datetime
import PyRSS2Gen
import db
import os
import config
from urlparse import urlparse, urlunparse


def process_playlists():
    playlists = db.get_all_playlists()
    for playlist in playlists:
        print 'Generating xml for "' + playlist['title'] + '"'
        generate_xml(playlist)


def generate_xml(playlist):
    base_url = config.get_option('FILES_URL')
    items = []

    downloaded_videos = db.get_downloaded_videos(2, playlist['id'])

    for video in downloaded_videos:
        link = "https://www.youtube.com/watch?v=" + video['yid']
        full_path = config.get_path('mp3', playlist['title'])
        full_path = os.path.join(full_path, video['filename'])
        url_parts = list(urlparse(base_url))
        url_parts[2] = os.path.join(url_parts[2], playlist['title'])
        url_parts[2] = os.path.join(url_parts[2], video['filename'])
        url = urlunparse(url_parts)
        info = PyRSS2Gen.RSSItem(
            title=video['title'],
            link=link,
            description=video['description'],
            guid=PyRSS2Gen.Guid(link),
            enclosure=PyRSS2Gen.Enclosure(url.replace('#', '%23'), os.path.getsize(full_path), "audio/mpeg"),
            pubDate=video['pubDate'])
        items.append(info)

    rss = PyRSS2Gen.RSS2(
        title=playlist['title'],
        link=config.get_option('PLAYLIST_BASE_URL') + playlist['yid'],
        language='en-us',
        description="",
        lastBuildDate=datetime.datetime.now(),
        items=items)
    rss.write_xml(open(config.get_path(None, playlist['title'] + '.xml'), "w"))
