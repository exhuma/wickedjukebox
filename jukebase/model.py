from model import Base
from sqlalchemy.types import (
        Integer,
        Unicode,
        Date,
        String,
        Boolean,
        Float,
        DateTime,
        )
from sqlalchemy.orm import (
        relationship,
        )
from sqlalchemy import (
        UniqueConstraint,
        Column,
        ForeignKey,
        Index,
        func,
        Table,
        PrimaryKeyConstraint
        )

ALBUM_TYPE_ALBUM="album"

channel_album_data = Table("channel_album_data", Base.metadata,
    Column('channel_id', Integer, ForeignKey("channel.id"), nullable=False),
    Column('album_id', Integer, ForeignKey("album.id"), nullable=False),
    Column('played', Integer, nullable=False, default=0),
    PrimaryKeyConstraint('channel_id', 'album_id')
    )

channel_song_data = Table("channel_song_data", Base.metadata,
    Column('channel_id', Integer, ForeignKey('channel.id'), nullable=False),
    Column('song_id', Integer, ForeignKey('song.id'), nullable=False),
    Column('played', Integer, nullable=False, default=0),
    Column('voted', Integer, nullable=False, default=0),
    Column('skipped', Integer, nullable=False, default=0),
    Column('lastPlayed', DateTime, default=None),
    Column('cost', Integer, default=5),
    PrimaryKeyConstraint('channel_id', 'song_id')
    )

song_has_genre = Table("song_has_genre", Base.metadata,
    Column('song_id', Integer, ForeignKey('song.id'), nullable=False),
    Column('genre_id', Integer, ForeignKey('genre.id'), nullable=False),
    PrimaryKeyConstraint('song_id', 'genre_id')
    )

song_has_tag = Table("song_has_tag", Base.metadata,
    Column('song_id', Integer, nullable=False),
    Column('tag', String(32), ForeignKey('tag.name'), nullable=False),
    PrimaryKeyConstraint('song_id', 'tag')
    )

#user_album_stats = Table("user_album_stats", Base.metadata,
#    Column('user_id', Integer, ForeignKey('user.id'), Integer, nullable=False),
#    Column('album_id', ForeignKey('album.id'), Integer, nullable=False),
#    Column('when', DateTime, nullable=False),
#    PrimaryKeyConstraint('user_id', 'album_id')
#    )

user_song_standing = Table("user_song_standing", Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('song_id', Integer, ForeignKey('song.id'), nullable=False),
    Column('standing', String(12), nullable=False),
    PrimaryKeyConstraint('user_id', 'song_id')
    )

user_song_stats = Table("user_song_stats", Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('song_id', Integer, ForeignKey('song.id'), nullable=False),
    Column('when', DateTime, nullable=False),
    PrimaryKeyConstraint('user_id', 'song_id', 'when')
    )

class Album(Base):
    __tablename__ = "album"
    __table_args__ = (
            UniqueConstraint('path'),
            Index('artist_id'),
            Index('name'),
            Index('type'),
            )
    id = Column(Integer, nullable=False, primary_key=True)
    artist_id = Column(Integer, ForeignKey('artist.id'), nullable=False)
    name = Column(Unicode(128), default=None)
    release_date = Column(Date, default=None)
    added = Column(DateTime, default=None)
    downloaded = Column(Integer, nullable=False, default=0)
    type = Column(String(32), nullable=False, default=ALBUM_TYPE_ALBUM)
    path = Column(Unicode(255), nullable=False)

class Artist(Base):
    __tablename__ = "artist"
    __table_args__ = (
            UniqueConstraint('name'),
            )
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Unicode(128), default=None)
    added = Column(DateTime, nullable=False)

class Channel(Base):
    __tablename__ = "channel"
    __table_args__ = (
            UniqueConstraint('name'),
            )
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(Unicode(32), nullable=False)
    public = Column(Boolean, default=True)
    backend = Column(Unicode(64), nullable=False)
    backend_params = Column(Unicode, nullable=False, default='')
    ping = Column(DateTime, default=None)
    active = Column(Boolean, default=False)
    status = Column(Integer, default=None)

class DynamicPlaylist(Base):
    __tablename__ = "dynamicPlaylist"
    id = Column(Integer, nullable=False, primary_key=True)
    channel_id = Column(Integer, default=None)
    group_id = Column(Integer, nullable=False)
    probability = Column(Float, nullable=False) # COMMENT 'Probability at which a song is picked from the playlisy (0.0-1.0)',
    label = Column(Unicode(64), default=None)
    query = Column(Unicode)

class Event(Base):
    __tablename__ = "events"
    __table_args__ = (
            Index('startdate', 'enddate'),
            )
    id = Column(Integer, nullable=False, primary_key=True)
    title = Column(Unicode, nullable=False)
    startdate = Column(DateTime, nullable=False)
    enddate = Column(DateTime, nullable=False)
    lat = Column(Float, default=None)
    lon = Column(Float, default=None)

class Genre(Base):
    __tablename__ = "genre"
    __table_args__ = (
            UniqueConstraint('name'),
            )
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(Unicode(128), default=None)
    added = Column(DateTime, nullable=False)

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, nullable=False, primary_key=True)
    title = Column(Unicode(32), nullable=False)
    admin = Column(Boolean, nullable=False, default=False)
    nocredits = Column(Integer, nullable=False, default=0)
    queue_skip = Column(Integer, nullable=False, default=0)
    queue_remove = Column(Integer, nullable=False, default=0)
    queue_add = Column(Integer, nullable=False, default=0)

class Lastfm_queue(Base):
    __tablename__ = "lastfm_queue"
    __table_args__ = (
            Index('song_id'),
            )
    queue_id = Column(Integer, nullable=False, primary_key=True)
    song_id = Column(Integer, ForeignKey('song.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    time_played = Column(DateTime, nullable=False)
    time_started = Column(DateTime, nullable=False)

class Log(Base):
    __tablename__ = "log"
    priority = Column(Unicode(32), nullable=False)
    message = Column(Unicode, nullable=False)
    date = Column(DateTime, nullable=False, default=func.now(), primary_key=True)

class Queue(Base):
    __tablename__ = "queue"
    __table_args__ = (
            Index('song_id'),
            Index('user_id'),
            Index('channel_id'),
            )
    id = Column(Integer, primary_key=True, nullable=False)
    song_id = Column(Integer, ForeignKey('song.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', onupdate="CASCADE", ondelete="CASCADE"), default=None)
    channel_id = Column(Integer, ForeignKey('channel.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    position = Column(Integer, default=0)
    added = Column(DateTime, nullable=False)

class RenderPreset(Base):
    __tablename__ = "render_presets"
    __table_args__ = (
            Index('cateory', 'preset'),
            )
    id = Column(Integer, primary_key=True, nullable=False)
    category = Column(Unicode(64), nullable=False)
    preset = Column(Unicode(64), nullable=False)
    hmax = Column(Integer, nullable=False)
    wmax = Column(Integer, nullable=False)
    placeholder = Column(Unicode(64), default=None)
    noproportion = Column(Boolean, nullable=False, default=False)
    force_mime = Column(String(16), nullable=False)

class Setting(Base):
    __tablename__ = "setting"
    __table_args__ = (
            PrimaryKeyConstraint('var', 'channel_id', 'user_id'),
            Index('channel_id'),
            Index('user_id')
            )
    var = Column(Unicode(32), nullable=False)
    value = Column(Unicode)
    channel_id = Column(Integer, ForeignKey( 'channel.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False, default=0)
    user_id = Column(Integer, ForeignKey( 'user.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False, default=0)

class SettingText(Base):
    __tablename__ = "setting_text"
    var = Column(Unicode(32), ForeignKey('setting.var'), nullable=False, primary_key=True)
    text_en = Column(Unicode, nullable=False)

class Shoutbox(Base):
    __tablename__ = "shoutbox"
    __table_args__ = (
            Index('added'),
            Index('user_id'),
            )
    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    message = Column(Unicode(255), nullable=False)
    added = Column(DateTime, nullable=False)

class Song(Base):
    __tablename__ = "song"
    __table_args__ = (
            UniqueConstraint('localpath'),
            )
    id = Column(Integer, nullable=False, primary_key=True)
    artist_id = Column(Integer, ForeignKey('artist.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    album_id = Column(Integer, ForeignKey('album.id', onupdate="CASCADE", ondelete="CASCADE"), default=None)
    track_no = Column(Integer, default=None)
    title = Column(Unicode(128), default=None)
    duration = Column(Float, default=None)
    year = Column(Integer, default=None)
    localpath = Column(Unicode(255), nullable=False)
    downloaded = Column(Integer, default=0)
    lastScanned = Column(DateTime, default=None)
    bitrate = Column(Integer, default=None)
    filesize = Column(Integer, default=None)
    checksum = Column(String(14), default=None)
    lyrics = Column(Unicode)
    broken = Column(Boolean, default=0)
    dirty = Column(Boolean, default=0)
    added = Column(DateTime, nullable=False)
    genres = relationship('genre', secondary=song_has_genre)
    tags = relationship('tag', secondary=song_has_tag)

class State(Base):
    __tablename__ = "state"
    channel_id = Column(Integer, nullable=False, primary_key=True)
    state = Column(String(64), primary_key=True, nullable=False)
    value = Column(String(255), default=None)

class Tag(Base):
    __tablename__ = "tag"
    label = Column(Unicode(32), primary_key=True, nullable=False)
    inserted = Column(DateTime, nullable=False, default=func.now())
    modified = Column(DateTime, nullable=False, default='0000-00-00 00:00:00')

class Users(Base):
    __tablename__ = "users"
    __table_args__ = (
            UniqueConstraint('username'),
            UniqueConstraint('cookie'),
            )
    id = Column(Integer, nullable=False, primary_key=True)
    username = Column(Unicode(32), nullable=False)
    cookie = Column(Unicode(32), nullable=False)
    password = Column(Unicode(32), nullable=False)
    fullname = Column(Unicode(64), nullable=False)
    email = Column(Unicode(128), nullable=False)
    credits = Column(Integer, nullable=False)
    group_id = Column(Integer, ForeignKey('group.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    downloads = Column(Integer, nullable=False, default=0)
    votes = Column(Integer, nullable=False, default=0)
    skips = Column(Integer, nullable=False, default=0)
    selects = Column(Integer, nullable=False, default=0)
    added = Column(DateTime, nullable=False)
    proof_of_life = Column(DateTime, nullable=False)
    proof_of_listening = Column(DateTime, default=None)
    ip = Column(Unicode(32), nullable=False)
    picture = Column(Unicode(255), nullable=False)
    lifetime = Column(Integer, nullable=False)
    channel_id = Column(Integer, nullable=False, default=1)

