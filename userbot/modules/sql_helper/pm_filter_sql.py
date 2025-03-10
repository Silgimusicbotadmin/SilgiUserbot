from sqlalchemy import Column, String, Integer
from userbot.modules.sql_helper import BASE, SESSION

class PMFilters(BASE):
    __tablename__ = "pm_filters"
    keyword = Column(String, primary_key=True)
    reply = Column(String)
    f_mesg_id = Column(Integer, nullable=True)

    def __init__(self, keyword, reply, f_mesg_id=None):
        self.keyword = keyword
        self.reply = reply
        self.f_mesg_id = f_mesg_id

PMFilters.__table__.create(checkfirst=True)

def add_pm_filter(keyword, reply, f_mesg_id=None):
    filter_ = PMFilters(keyword, reply, f_mesg_id)
    SESSION.add(filter_)
    SESSION.commit()

def get_pm_filters():
    return SESSION.query(PMFilters).all()

def remove_pm_filter(keyword):
    filter_ = SESSION.query(PMFilters).filter_by(keyword=keyword).first()
    if filter_:
        SESSION.delete(filter_)
        SESSION.commit()
        return True
    return False
