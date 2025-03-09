# ⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝
try:
    from userbot.modules.sql_helper import SESSION, BASE
except ImportError:
    raise AttributeError
from sqlalchemy import Column, String, UnicodeText, Integer

class PMFilters(BASE):
    __tablename__ = "pm_filters"
    keyword = Column(String(50), primary_key=True)
    reply = Column(UnicodeText)
    f_mesg_id = Column(Integer, nullable=True)

    def __init__(self, keyword, reply, f_mesg_id):
        self.keyword = keyword
        self.reply = reply
        self.f_mesg_id = f_mesg_id

PMFilters.__table__.create(checkfirst=True)

def add_pm_filter(keyword, reply, f_mesg_id=None):
    filter_exists = SESSION.query(PMFilters).get(keyword)
    if filter_exists:
        SESSION.delete(filter_exists)
    new_filter = PMFilters(keyword, reply, f_mesg_id)
    SESSION.add(new_filter)
    SESSION.commit()

def get_pm_filters():
    return SESSION.query(PMFilters).all()

def remove_pm_filter(keyword):
    filter_exists = SESSION.query(PMFilters).get(keyword)
    if filter_exists:
        SESSION.delete(filter_exists)
        SESSION.commit()
        return True
    return False
