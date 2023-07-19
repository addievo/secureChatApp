from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Message

engine = create_engine('sqlite:///chat.db')  # Use SQLite for simplicity
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def get_user(username):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    return user

def create_user(username, password_hash, public_key, private_key):
    session = Session()
    user = User(username=username, password_hash=password_hash, public_key=public_key, private_key=private_key)
    session.add(user)
    session.commit()
    session.close()

def get_message(message_id):
    session = Session()
    message = session.query(Message).filter_by(id=message_id).first()
    session.close()
    return message

def create_message(sender_id, receiver_id, content, timestamp):
    session = Session()
    message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content, timestamp=timestamp)
    session.add(message)
    session.commit()
    session.close()
