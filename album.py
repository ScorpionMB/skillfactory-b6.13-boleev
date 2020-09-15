import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from bottle import HTTPError
from bottle import response

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

def save(artist):
    """
    Производит запись в базу нового альбома
    """
    session = connect_db()

    if session.query(Album).filter(Album.artist == artist.artist, Album.album == artist.album).first():
        raise HTTPError(409, "Ошибка. Такой альбом уже есть в списке")
    else:
        session.add(artist)
        session.commit()
        return "Данные успешно сохранены"


