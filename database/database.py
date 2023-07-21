from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, User, Message

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


def update_user(username, new_username=None, new_password_hash=None, new_public_key=None, new_private_key=None,
                new_avatar=None, new_status=None):
    session = Session()
    user = session.query(User).filter_by(username=username).first()

    if user is None:
        session.close()
        return False

    if new_username is not None:
        user.username = new_username
    if new_password_hash is not None:
        user.password_hash = new_password_hash
    if new_public_key is not None:
        user.public_key = new_public_key
    if new_private_key is not None:
        user.private_key = new_private_key
    if new_avatar is not None:
        user.avatar = new_avatar
    if new_status is not None:
        user.status = new_status

    session.commit()
    session.close()
    return True


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
