from enum import Enum

from sqlalchemy import Column, Integer, BigInteger, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base


BaseModel = declarative_base()
__all__ = ["BaseModel", "ViewKindVariant", "User", "Chat", "ViewKind", "BotImg", "BotMsg", "CompanyText"]


class ViewKindVariant(Enum):
    MAIN_MENU = 0


class User(BaseModel):
    __tablename__ = 'user'

    telegram_id = Column(BigInteger, primary_key=True)
    chat_id = Column(BigInteger, ForeignKey('chat.id', ondelete="CASCADE"))
    is_active_in_telegram = Column(Boolean, nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=True)
    username = Column(String(32), nullable=True)
    phone = Column(String(15), nullable=True)

    chat = relationship('Chat', back_populates='user', uselist=False, lazy="noload")


class Chat(BaseModel):
    __tablename__ = 'chat'

    id = Column(BigInteger, primary_key=True)
    kind_id = Column(Integer, ForeignKey('view_kind.id', ondelete="RESTRICT"), default=0)
    content = Column(String(4096))
    sub_window_number = Column(Integer, default=1)

    view_kind = relationship('ViewKind', back_populates='chat', lazy="noload")
    user = relationship('User', back_populates='chat', lazy="noload")
    bot_img = relationship('BotImg', back_populates='chat', lazy="noload")
    bot_msg = relationship('BotMsg', back_populates='chat', lazy="noload")


class ViewKind(BaseModel):

    __tablename__ = 'view_kind'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    chat = relationship('Chat', back_populates='view_kind', lazy="noload")


class BotImg(BaseModel):
    __tablename__ = 'bot_img'

    rec_id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger, ForeignKey('chat.id', ondelete="CASCADE"))
    url = Column(String(65535))

    chat = relationship('Chat', back_populates='bot_img', lazy="noload")


class BotMsg(BaseModel):

    __tablename__ = 'bot_msg'
    rec_id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger, ForeignKey('chat.id', ondelete="CASCADE"))
    message_id = Column(Integer)

    chat = relationship('Chat', back_populates='bot_msg', lazy="noload")


class TextKindVariant(Enum):
    BOT_COMMAND_START = 1
    BOT_COMMAND_HELP = 2


class CompanyText(BaseModel):
    __tablename__ = 'company_text'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=True, default=None)
    text = Column(String(4096))
