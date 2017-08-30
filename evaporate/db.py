from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, UniqueConstraint, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import config
import os

Base = declarative_base()
path = config.get_db_path()
URI = 'sqlite:///' + path


class Video(Base):
    __tablename__ = 'video'
    id = Column(Integer, primary_key=True)
    yid = Column(String, unique=True)
    title = Column(String)
    description = Column(String)
    pubDate = Column(DateTime)


def create_db():
    if not os.path.exists(path):
        engine = create_engine(URI)
        Base.metadata.create_all(engine)


def add_video(info):
    engine = create_engine(URI)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    result = session.query(Video).filter_by(yid=info['yid']).first()
    datetime.now()
    if not result:
        pubDate = datetime.strptime(info['pubDate'], '%Y%m%d')
        new_video = Video(yid=info['yid'], title=info['title'], description=info['description'], pubDate=pubDate)
        session.add(new_video)
        session.commit()
    result = session.query(Video).filter_by(yid=info['yid']).first()
    return result.id


def get_downloaded_videos(option):
    # 1: return yids, 2: return all
    engine = create_engine(URI)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    result = session.query(Video).all()
    downloaded_videos = []
    for row in result:
        if option == 1:
            downloaded_videos.append(row.yid)
        elif option == 2:
            downloaded_videos.append(row.__dict__)
    return downloaded_videos
