import datetime
import PyRSS2Gen
import db
import os
import config


def generate_xml():
    url = config.get_option('FILES_URL')
    items = []

    downloaded_videos = db.get_downloaded_videos(2)

    for video in downloaded_videos:
        link = "https://www.youtube.com/watch?v=" + video['yid']
        filename = filename = str(video['id']) + '. ' + video['title'] + '.mp3'
        info = PyRSS2Gen.RSSItem(
            title=video['title'],
            link=link,
            description=video['description'],
            guid=PyRSS2Gen.Guid(link),
            enclosure=PyRSS2Gen.Enclosure(url + filename.replace('#', '%23'), os.path.getsize(config.get_path('mp3', filename)), "audio/mpeg"),
            pubDate=video['pubDate'])
        items.append(info)

    rss = PyRSS2Gen.RSS2(
        title="MC",
        link="https://www.youtube.com/playlist?list=PLlUk42GiU2guNzWBzxn7hs8MaV7ELLCP_",
        language='en-us',
        description="Running the game",
        lastBuildDate=datetime.datetime.now(),
        items=items)

    rss.write_xml(open(config.get_path(None, 'evaporate.xml'), "w"))
