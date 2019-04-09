from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import asc, or_

from db_model import get_engine, User, Schedule
from db_log import error
import datetime
Base = declarative_base()
ENGINE = get_engine()
Base.metadata.bind = ENGINE
DBSession = sessionmaker(bind=ENGINE)
    
def insert_object(object):
    session = DBSession()
    try:
        session.add(object)
        session.commit()
    except Exception as e:
        error('error at inserting object')
        error('error info: %s' % str(e))
        session.rollback()
    finally:
        session.close()

def insert_list_object(list_object):
    session = DBSession()
    try:
        session.bulk_save_objects(list_object)
        session.commit()
    except Exception as e:
        error('exxor at inserting %d objects' % len(list_object))
        error('error info: %s' % str(e))
        session.rollback()
    finally:
        session.close()


#-----------user


def get_user_id(face_id):
    session = DBSession()
    try:
        query = session.query(User).filter_by(face_id=face_id)
        records = query.all()
        if len(records) < 1:
            error('Cant find user has face_id: %s' % str(face_id))
    except Exception as e:
        error('error info: %s' % str(e))
        error('error at get_user_by_id id of user: %s'%face_id)
        records = []
    finally:
        session.close()
    return records

def get_all_user(face_id=None, start=None, end=None):
    session = DBSession()
    try:
        if face_id is not None:
            records = session.query(User)\
                .filter(User.face_id == face_id)\
                .order_by(asc(User.face_id)).all()
        elif start is not None and end is not None:
            records = session.query(User) \
                .filter(or_(User.date_created > start, User.date_created == start)) \
                .filter(User.date_created < end) \
                .order_by(asc(User.face_id)).all()
        else:
            records = session.query(User) \
                .order_by(asc(User.face_id)).all()
    except Exception as e:
        error('error info: %s' % str(e))
        error('error at get_all_user')
        records = []
    finally:
        session.close()
    return records

def update_user(face_id, avatar):
    session = DBSession()
    try:
        session.query(User).filter_by(face_id=face_id).update({"avatar": avatar})
        session.commit()
    except Exception as e:
        error('error at update_schedule object')
        error('error info: %s' % str(e))
        session.rollback()
    finally:
        session.close()


#---------schedule


def check_schedule(date, user_id):
    session = DBSession()
    try:
        records = session.query(Schedule).filter_by(date=date, user_id=user_id).all()
    except Exception as e:
        error('error info: %s' % str(e))
        error('error at check_user_by_date_and_user with date: {0}; user_id: {1}'.format(date, user_id))
        records = []
    finally:
        session.close()
    return records

def update_schedule(schedule):
    session = DBSession()
    try:
        session.query(Schedule).filter_by(date=schedule.date, user_id=schedule.user_id).update({"end_time": schedule.end_time, "modify": schedule.modify})
        session.commit()
    except Exception as e:
        error('error at update_schedule object')
        error('error info: %s' % str(e))
        session.rollback()
    finally:
        session.close()


if __name__ == '__main__':
    
    tuanlv = User(face_id='tuanlv', password='tuanlv', date_created = str(datetime.datetime.now()), level=1, fullname='Le Van Tuan', avatar= '/images/avatar/Tuanlv/0.jpg')
    insert_object(tuanlv)


    # s1 = Schedule(user_id=1, date=20181010, start='8:30:00', end='17:30:00', url_image='test', modify='17:30:00')
    # s2 = Schedule(user_id=1, date=20181011, start='8:30:00', end='17:30:00', url_image='test', modify='17:30:00')
    # s3 = Schedule(user_id=2, date=20181010, start='9:00:00', end='17:30:00', url_image='test', modify='17:30:00')
    # s4 = Schedule(user_id=2, date=20181011, start='9:30:00', end='17:30:00', url_image='test', modify='17:30:00')
    # s5 = Schedule(user_id=3, date=20181010, start='9:15:00', end='17:30:00', url_image='test', modify='17:30:00')
    # s6 = Schedule(user_id=3, date=20181011, start='10:00:00', end='17:30:00', url_image='test', modify='17:30:00')
    # insert_object(s1)
    # insert_object(s2)
    # insert_object(s3)
    # insert_object(s4)
    # insert_object(s5)
    # insert_object(s6)


    # Bienpt = User(face_id='Bienpt', fullname='Phan Trong Bien', avatar='/api/avatars/Bientpt.jpg')
    # Datnv = User(face_id='Datnv', fullname='Nguyen Van Dat', avatar='/api/avatars/Datnv/0.jpg')
    # Diepct = User(face_id='Diepct', fullname='Cu Thi Diep', avatar='/api/avatars/Diepct/0.jpg')
    # Diepnv = User(face_id='Diepnv', fullname='Nguyen Van Diep', avatar='/api/avatars/Diepnv/0.jpg')
    # Ducpv = User(face_id='Ducpv', fullname='Pham Trong Duc',avatar= '/api/avatars/Ducpv/0.jpg')
    # Dungnt2 = User(face_id='Dungnt2', fullname='Nguyen Dung',avatar= '/api/avatars/Dungnt2/0.jpg')
    # HoangAnh = User(face_id='HoangAnh', fullname='Hoang Thi Anh',avatar= '/api/avatars/HoangAnh/0.jpg')
    # Hungpb = User(face_id='Hungpb', fullname='Pham Ba Hung',avatar= '/api/avatars/Hungpb/0.jpg')
    # Huudv = User(face_id='Huudv', fullname='Do Van Huu', avatar='/api/avatars/Huudv/0.jpg')
    # Lanhnt = User(face_id='Lanhnt', fullname='Nguyen Thi Lanh',avatar= '/api/avatars/Lanhnt/0.jpg')
    # Lienbp = User(face_id='Lienbp', fullname='Bui Phuong Lien', avatar='/api/avatars/Lienbp/0.jpg')
    # Locnt = User(face_id='Locnt', fullname='Nguyen Thi Loc',avatar= '/api/avatars/Locnt/0.jpg')
    # Luanvv = User(face_id='Luanvv', fullname='Vu Van Luan',avatar= '/api/avatars/Luanvv/0.jpg')
    # Lucnv = User(face_id='Lucnv', fullname='Nguyen Van Luc', avatar='/api/avatars/Lucnv/0.jpg')
    # Luongvh = User(face_id='Luongvh', fullname='Vu Hien Luong',avatar= '/api/avatars/Luongvh/0.jpg')
    # Ngannt = User(face_id='Ngannt', fullname='Nguyen Thi Ngan', avatar='/api/avatars/Ngannt/0.jpg')
    # phuongdv = User(face_id='phuongdv', fullname='Dang Van Phuong',avatar= '/api/avatars/phuongdv/0.jpg')
    # Quynhtt = User(face_id='Quynhtt', fullname='Tran Thi Quynh', avatar='/api/avatars/Quynhtt/0.jpg')
    # Sonnh = User(face_id='Sonnh', fullname='Nguyen Huy Son', avatar='/api/avatars/Sonnh/0.jpg')
    # Sonnv = User(face_id='Sonnv', fullname='Nguyen Van Son', avatar='/api/avatars/Sonnv/0.jpg')
    # ThanhHoa = User(face_id='ThanhHoa', fullname='Thanh Hoa',avatar= '/api/avatars/ThanhHoa/0.jpg')
    # Thao = User(face_id='Thao', fullname='Thao', avatar='/api/avatars/Thao/0.jpg')
    # Thuannq = User(face_id='Thuannq', fullname='Nguyen Quang Thuan',avatar= '/api/avatars/Thuannq/0.jpg')
    # Truongtx = User(face_id='Truongtx', fullname='Tong Xuan Truong', avatar='/api/avatars/Truongtx/0.jpg')
    # TuanAnh = User(face_id='TuanAnh', fullname='Tuan Anh', avatar='/api/avatars/TuanAnh/0.jpg')
    # tuanlv = User(face_id='tuanlv', fullname='Le Van Tuan',avatar= '/api/avatars/tuanlv/0.jpg')
    # Tungds = User(face_id='Tungds', fullname='Do Son Tung', avatar='/api/avatars/Tungds/0.jpg')
    # Tungnt = User(face_id='Tungnt', fullname='Nguyen Thanh Tung', avatar='/api/avatars/Tungnt/0.jpg')
    # VietAnh = User(face_id='VietAnh', fullname='Viet Anh',avatar= '/api/avatars/VietAnh/0.jpg')
    # Vietdb = User(face_id='Vietdb', fullname='Duong Bao Viet',avatar= '/api/avatars/Vietdb/0.jpg')
    # insert_object(Bienpt)
    # insert_object(Datnv)
    # insert_object(Diepct)
    # insert_object(Diepnv)
    # insert_object(Ducpv)
    # insert_object(Dungnt2)
    # insert_object(HoangAnh)
    # insert_object(Hungpb)
    # insert_object(Huudv)
    # insert_object(Sonnh)
    # insert_object(Lanhnt)
    # insert_object(Lienbp)
    # insert_object(Locnt)
    # insert_object(Luanvv)
    # insert_object(Lucnv)
    # insert_object(Luongvh)
    # insert_object(Ngannt)
    # insert_object(phuongdv)
    # insert_object(Quynhtt)
    # insert_object(Sonnv)
    # insert_object(ThanhHoa)
    # insert_object(Thao)
    # insert_object(Thuannq)
    # insert_object(Truongtx)
    # insert_object(TuanAnh)
    # insert_object(tuanlv)
    # insert_object(Tungds)
    # insert_object(Tungnt)
    # insert_object(VietAnh)
    # insert_object(Vietdb)

