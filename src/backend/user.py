import argparse
from db_session import insert_object, get_user_id
from db_model import User
import datetime
import os

FOLDER_CURR = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--id", type=str,
	help="id of user")
ap.add_argument("-n", "--name", type=str,
	help="name of user")

args = vars(ap.parse_args())
id = args["id"]
name = args["name"]
records = get_user_id(name)
if len(records) > 0:
    print('user is exist!')
else:
    folder = os.path.join(FOLDER_CURR, '..', 'datasets')
    path = os.path.join(folder, name)
    avatar = '/images/avatar/{0}/0.jpg'.format(name)
    if not os.path.isdir(path):
        os.mkdir(path)
    user = User(face_id=id, password=id, date_created = str(datetime.datetime.now()), level=1, fullname=name, avatar= avatar)
    insert_object(user)