# ⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝
try:
    from userbot.modules.sql_helper import SESSION, BASE
except ImportError:
    raise AttributeError
from sqlalchemy import Column, String, UnicodeText, Integer

class PMFilters(BASE):
    __tablename__ = "pm_filters"
    id = Column(Integer, primary_key=True, autoincrement=True)
    keyword = Column(String(50), unique=True, nullable=False)
    reply = Column(UnicodeText, nullable=False)
    f_mesg_id = Column(Integer, nullable=True)

    def __init__(self, keyword, reply, f_mesg_id=None):
        self.keyword = keyword
        self.reply = reply
        self.f_mesg_id = f_mesg_id

PMFilters.__table__.create(checkfirst=True)

def add_pm_filter(keyword, reply, f_mesg_id=None):
    existing_filter = SESSION.query(PMFilters).filter_by(keyword=keyword).first()
    if existing_filter:
        SESSION.delete(existing_filter)

    new_filter = PMFilters(keyword, reply, f_mesg_id)
    SESSION.add(new_filter)
    SESSION.commit()

def get_pm_filters():
    return SESSION.query(PMFilters).all()

def remove_pm_filter(keyword):
    filter_to_remove = SESSION.query(PMFilters).filter_by(keyword=keyword).first()
    if filter_to_remove:
        SESSION.delete(filter_to_remove)
        SESSION.commit()
        return True
    return False
