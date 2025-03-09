# ⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝
try:
    from userbot.modules.sql_helper import SESSION, BASE
except ImportError:
    raise AttributeError

from sqlalchemy import Column, UnicodeText, String, Integer


class PMFilters(BASE):
    __tablename__ = "pm_filters"
    user_id = Column(String(14), primary_key=True)  # Hər user üçün fərdi saxlanacaq
    keyword = Column(UnicodeText, primary_key=True, nullable=False)
    reply = Column(UnicodeText)
    f_mesg_id = Column(Integer, nullable=True)

    def __init__(self, user_id, keyword, reply, f_mesg_id):
        self.user_id = str(user_id)
        self.keyword = keyword
        self.reply = reply
        self.f_mesg_id = f_mesg_id

    def __eq__(self, other):
        return bool(
            isinstance(other, PMFilters)
            and self.user_id == other.user_id
            and self.keyword == other.keyword
        )


PMFilters.__table__.create(checkfirst=True)


def get_pm_filter(user_id, keyword):
    try:
        return SESSION.query(PMFilters).get((str(user_id), keyword))
    finally:
        SESSION.close()


def get_pm_filters(user_id):
    try:
        return SESSION.query(PMFilters).filter(PMFilters.user_id == str(user_id)).all()
    finally:
        SESSION.close()


def add_pm_filter(user_id, keyword, reply, f_mesg_id):
    to_check = get_pm_filter(user_id, keyword)
    if not to_check:
        adder = PMFilters(str(user_id), keyword, reply, f_mesg_id)
        SESSION.add(adder)
        SESSION.commit()
        return True
    else:
        rem = SESSION.query(PMFilters).get((str(user_id), keyword))
        SESSION.delete(rem)
        SESSION.commit()
        adder = PMFilters(str(user_id), keyword, reply, f_mesg_id)
        SESSION.add(adder)
        SESSION.commit()
        return False


def remove_pm_filter(user_id, keyword):
    to_check = get_pm_filter(user_id, keyword)
    if not to_check:
        return False
    else:
        rem = SESSION.query(PMFilters).get((str(user_id), keyword))
        SESSION.delete(rem)
        SESSION.commit()
        return True
