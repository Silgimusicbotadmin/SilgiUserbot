from sqlalchemy import Column, UnicodeText, Numeric, String
from userbot.modules.sql_helper import BASE, SESSION

class PMMessageFilters(BASE):
    __tablename__ = "pm_message_filters"  
    chat_id = Column(String(14), primary_key=True)
    keyword = Column(UnicodeText, primary_key=True, nullable=False)
    reply = Column(UnicodeText)
    f_mesg_id = Column(Numeric)

    def __init__(self, chat_id, keyword, reply, f_mesg_id):
        self.user_id = str(chat_id)
        self.keyword = keyword
        self.reply = reply
        self.f_mesg_id = f_mesg_id

    def __eq__(self, other):
        return bool(
            isinstance(other, PMMessageFilters) and self.chat_id == other.chat_id
            and self.keyword == other.keyword)

PMMessageFilters.__table__.create(checkfirst=True)

def get_pm_filter(chat_id, keyword):
    try:
        return SESSION.query(PMMessageFilters).get((str(chat_id), keyword))
    finally:
        SESSION.close()
def get_pm_filters(chat_id):
    try:
        return SESSION.query(PMMessageFilters).filter(
            PMMessageFilters.chat_id == str(chat_id)).all()
    finally:
        SESSION.close()
def add_pm_filter(chat_id, keyword, reply, f_mesg_id):
    to_check = get_pm_filter(chat_id, keyword)
    if not to_check:
        adder = PMMessageFilters(str(chat_id), keyword, reply, f_mesg_id)
        SESSION.add(adder)
        SESSION.commit()
        return True
    else:
        rem = SESSION.query(PMMessageFilters).get((str(chat_id), keyword))
        SESSION.delete(rem)
        SESSION.commit()
        adder = PMMessageFilters(str(chat_id), keyword, reply, f_mesg_id)
        SESSION.add(adder)
        SESSION.commit()
        return False
def remove_pm_filter(chat_id, keyword):
    to_check = get_pm_filter(chat_id, keyword)
    if not to_check:
        return False
    else:
        rem = SESSION.query(PMMessageFilters).get((str(chat_id), keyword))
        SESSION.delete(rem)
        SESSION.commit()
        return True
