from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import anisong


Base = declarative_base()
engine = create_engine("sqlite:///malsongs.sqlite")
Session = sessionmaker(bind=engine)
session = Session()


class Songs(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True)
    anime = Column(String)
    type = Column(String)
    number = Column(Integer)
    title = Column(String)
    artist = Column(String)
    used_in_eps = Column(String)
    status = Column(Integer)


def create_table():
    """Create tables in database if they doesn't exist"""
    Base.metadata.create_all(engine)


def get_all_anisongs():
    """Get all anisongs in database"""
    anisongs = list()
    for result in session.query(Songs).order_by(Songs.anime):
        anisongs.append(anisong.Anisong.from_database_query(result))
    return anisongs


def generate_db_objects_for_anisongs(anisongs):
    for song in filter(lambda x: not x.database_obj, anisongs):
        song.database_obj = Songs(anime=song.anime.anime_name,
                                  type=song.type,
                                  number=song.number,
                                  title=song.title,
                                  artist=song.artist,
                                  used_in_eps=song.used_in_eps,
                                  status=0)
