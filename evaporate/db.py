from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import config
import os

Base = declarative_base()
path = config.get_db_path()
URI = 'sqlite:///' + path


class Video(Base):
    __tablename__ = 'video'
    id = Column(Integer, primary_key=True)
    yid = Column(String)
    playlist_id = Column(Integer, ForeignKey("playlist.id"), nullable=False)
    title = Column(String)
    episode_number = Column(Integer)
    description = Column(String)
    pubDate = Column(DateTime)
    filename = Column(String)


class Playlist(Base):
    __tablename__ = 'playlist'
    id = Column(Integer, primary_key=True)
    yid = Column(String, unique=True)
    title = Column(String)
    videos = relationship("Video", cascade="all,delete", backref="playlist")


def create_db():
    if not os.path.exists(path):
        engine = create_engine(URI)
        Base.metadata.create_all(engine)


def get_session():
    engine = create_engine(URI)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()


def add_playlist(info):
    session = get_session()
    result = session.query(Playlist).filter_by(yid=info['id']).first()
    if not result:
        new_playlist = Playlist(yid=info['id'], title=info['title'])
        session.add(new_playlist)
        session.commit()


def get_all_playlists():
    session = get_session()
    result = session.query(Playlist).all()
    playlists = []
    for row in result:
        playlists.append(row.__dict__)
    return playlists


def get_playlist(playlist_id):
    session = get_session()
    result = session.query(Playlist).filter_by(id=playlist_id).first()
    if result:
        return result.__dict__


def remove_playlist(playlist_id):
    session = get_session()
    result = session.query(Playlist).filter_by(id=playlist_id).first()
    session.delete(result)
    session.commit()


def add_video(info):
    session = get_session()
    result = session.query(Video).filter_by(yid=info['yid']).first()
    if not result:
        pubDate = datetime.strptime(info['pubDate'], '%Y%m%d')
        new_video = Video(yid=info['yid'], title=info['title'], description=info['description'], pubDate=pubDate, playlist_id=info['playlist_id'], episode_number=info['episode_number'], filename=info['filename'])
        session.add(new_video)
        session.commit()
    result = session.query(Video).filter_by(yid=info['yid']).first()
    return result.id


def get_downloaded_videos(option, playlist_id):
    # 1: return yids, 2: return all
    session = get_session()
    result = session.query(Video).filter_by(playlist_id=playlist_id).all()
    downloaded_videos = []
    for row in result:
        if option == 1:
            downloaded_videos.append(row.yid)
        elif option == 2:
            downloaded_videos.append(row.__dict__)
    return downloaded_videos
