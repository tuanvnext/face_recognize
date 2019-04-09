import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, Float, String, Unicode, PrimaryKeyConstraint, Date, Time, Boolean, DateTime
from sqlalchemy.orm import relationship
from passlib.hash import bcrypt

Base = declarative_base()
ACCESS_FILE_PATH = os.path.dirname(os.path.abspath(__file__)) + '/access.txt'

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    face_id = Column(String(256), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    level = Column(Integer, nullable=False)
    fullname = Column(Unicode(256), nullable=False)
    date_created = Column(DateTime)
    avatar = Column(Unicode(256))
    def __init__(self, face_id, password, date_created, level = 1, fullname=None, avatar=None, ):
        self.face_id = face_id
        self.password = bcrypt.encrypt(password)
        self.level = level
        self.fullname = fullname
        self.avatar = avatar
        self.date_created = date_created

    def validate_password(self, password):
        return bcrypt.verify(password, self.password)

class Schedule(Base):
    __tablename__ = 'schedule'
    #uuid = Column('UUID', UUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey('user.id'))
    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    url_image = Column(Unicode(256), nullable=True)

    modify = Column(String(10000))
    user = relationship(User)
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'date'),
        {},
    )

    def __init__(self, user_id, date, start, end, url_image, modify):
        self.user_id = user_id
        self.date = date
        self.start_time = start
        self.end_time = end
        self.modify = modify
        self.url_image = url_image


def read_file_config():
    result = {}
    f = open(ACCESS_FILE_PATH, 'r')
    for line in f:
        temp = line.split(':')
        result[temp[0].strip()] = temp[1].strip()
    f.close()
    return result

CONFIG_DIC = read_file_config()

def get_engine():
    user_name = CONFIG_DIC['user']
    password = CONFIG_DIC['password']
    host = CONFIG_DIC['host']
    db_name = CONFIG_DIC['database']
    #mysql_engine_str = 'mysql+mysqldb://%s:%s@%s/%s?charset=utf8mb4' % (user_name, password, host, db_name)
    mysql_engine_str = 'mysql+mysqldb://%s:%s@%s/%s?charset=utf8' % (user_name, password, host, db_name)
    engine = create_engine(mysql_engine_str, pool_recycle=3600 * 7)
    return engine

def create_database():
    engine = get_engine()
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    create_database()

