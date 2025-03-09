# ⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝
try:
    from userbot.modules.sql_helper import SESSION, BASE
except ImportError:
    raise AttributeError
from sqlalchemy import Column, String, UnicodeText, Integer
class PMFilters(BASE):
    __tablename__ = "pm_filters"
    chat_id = Column(String(14), primary_key=True)
    keyword = Column(UnicodeText, primary_key=True)
    reply = Column(UnicodeText)
    f_mesg_id = Column(Integer, nullable=True)

    def __init__(self, chat_id, keyword, reply, f_mesg_id):
        self.chat_id = str(chat_id)
        self.keyword = keyword
        self.reply = reply
        self.f_mesg_id = f_mesg_id

PMFilters.__table__.create(checkfirst=True)

def add_pm_filter(chat_id, keyword, reply, f_mesg_id=None):
    filter_exists = SESSION.query(PMFilters).get((str(chat_id), keyword))
    if filter_exists:
        SESSION.delete(filter_exists)
    new_filter = PMFilters(str(chat_id), keyword, reply, f_mesg_id)
    SESSION.add(new_filter)
    SESSION.commit()

def get_pm_filters(chat_id):
    return SESSION.query(PMFilters).filter(PMFilters.chat_id == str(chat_id)).all()

def remove_pm_filter(chat_id, keyword):
    filter_exists = SESSION.query(PMFilters).get((str(chat_id), keyword))
    if filter_exists:
        SESSION.delete(filter_exists)
        SESSION.commit()
        return True
    return False
