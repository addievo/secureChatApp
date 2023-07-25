from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    public_key = Column(String, nullable=False)
    private_key = Column(String, nullable=False)
    avatar = Column(String)
    status = Column(String)

    messages_sent = relationship("Message", backref='sender', foreign_keys='Message.sender_id')
    messages_received = relationship("Message", backref='receiver', foreign_keys='Message.receiver_id')


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'))
    receiver_id = Column(Integer, ForeignKey('users.id'))
    content_for_sender = Column(String, nullable=False)
    content_for_receiver = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
