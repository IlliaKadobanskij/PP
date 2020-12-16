from database import db_session
from models import Users, PlayList, Video
from database import init_db

init_db()

# u = Users('admin3', password=1234)
#
# db_session.add(u)
#
# db_session.commit()

p = PlayList(name='bot')
c = Video(url='https://www.youtube.com/watch?v=v0Bu3M4r4K4', playlist=p)


db_session.add(p)
db_session.add(c)

db_session.commit()
