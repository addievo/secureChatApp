from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker, joinedload
from .models import Base, User, Message
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

engine = create_engine('sqlite:///active_database/chat.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


# serialising RSA keys while loading from database
# added id = user.id
def get_user(username, user_id=None):
    session = Session()
    if user_id:
        user = session.query(User).filter_by(id=user_id).first()
    else:
        user = session.query(User).filter_by(username=username).first()
    if user:
        public_key = serialization.load_pem_public_key(user.public_key.encode(), backend=default_backend())
        private_key = serialization.load_pem_private_key(user.private_key.encode(), password=None,
                                                         backend=default_backend())
        user = User(id=user.id, username=user.username, password_hash=user.password_hash,
                    public_key=public_key, private_key=private_key, avatar=user.avatar, status=user.status)
    session.close()
    return user


# editing create user to convert RSA keys to strings before saving
def create_user(username, password_hash, public_key, private_key):
    session = Session()
    public_key_string = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                format=serialization.PublicFormat.SubjectPublicKeyInfo).decode('utf-8')
    private_key_string = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                   format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                   encryption_algorithm=serialization.NoEncryption()).decode('utf-8')
    user = User(username=username, password_hash=password_hash, public_key=public_key_string,
                private_key=private_key_string)
    session.add(user)
    session.commit()
    session.close()


# editing update user to convert RSA keys to strings before saving
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
        public_key_string = new_public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                        format=serialization.PublicFormat.SubjectPublicKeyInfo).decode(
            'utf-8')
        user.public_key = public_key_string
    if new_private_key is not None:
        private_key_string = new_private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                           format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                           encryption_algorithm=serialization.NoEncryption()).decode(
            'utf-8')
        user.private_key = private_key_string
    if new_avatar is not None:
        user.avatar = new_avatar
    if new_status is not None:
        user.status = new_status

    session.commit()
    session.close()
    return True


# modifying to add joinedLoad to only load messages from same instance

# changing to get_messages_for_user_and_partner

def get_messages_for_user_and_partner(user_id, partner_id):
    session = Session()
    messages = session.query(Message).options(
        joinedload(Message.sender),
        joinedload(Message.receiver)
    ).filter(
        or_(
            and_(Message.sender_id == user_id, Message.receiver_id == partner_id),
            and_(Message.sender_id == partner_id, Message.receiver_id == user_id)
        )
    ).all()
    session.close()
    return messages


def create_message(sender_id, receiver_id, content_for_sender, content_for_receiver, timestamp):
    session = Session()
    message = Message(sender_id=sender_id, receiver_id=receiver_id, content_for_sender=content_for_sender,
                      content_for_receiver=content_for_receiver, timestamp=timestamp)
    session.add(message)
    session.commit()
    session.close()


def get_conversations_for_user(user_id):
    session = Session()
    sent_messages = session.query(Message).filter_by(sender_id=user_id).all()
    received_messages = session.query(Message).filter_by(receiver_id=user_id).all()
    session.close()

    # Get unique users from sent and received messages
    user_ids = set()
    for message in sent_messages:
        user_ids.add(message.receiver_id)
    for message in received_messages:
        user_ids.add(message.sender_id)

    # Get usernames corresponding to IDS
    usernames = []

    for user_id in user_ids:
        user = get_user(None, user_id)
        if user:
            usernames.append(user.username)

    return usernames
