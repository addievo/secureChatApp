from datetime import datetime
from flask import request, session, jsonify, render_template
from auth.middleware import require_login
from database.database import get_user, create_message, get_messages_for_user
from encryption.encryption import encrypt_message, decrypt_message
from flask import Blueprint
from flask import json

current_time = datetime.now()

bp = Blueprint('chat', __name__)


@bp.route('/send_message', methods=['POST'])
@require_login
def send_message():
    data = json.loads(request.data)
    sender_username = session['username']
    receiver_username = data['receiver_username']
    content = data['message']

    sender = get_user(sender_username)
    receiver = get_user(receiver_username)

    if receiver is None:
        return jsonify({"error": "Receiver does not exist"}), 400

    receiver_public_key = receiver.public_key
    encrypted_message = encrypt_message(receiver_public_key, content)
    create_message(sender.id, receiver.id, encrypted_message, current_time)
    return jsonify({"message": "Message sent successfully"}), 200


@bp.route('/get_messages', methods=['GET'])
@require_login
def get_messages():
    username = session['username']
    user = get_user(username)
    print("Current User = " + user.username)

    messages = get_messages_for_user(user.id)

    decrypted_messages = []
    for message in messages:
        sender = get_user(None, message.sender_id)
        receiver = get_user(None, message.receiver_id)
        print("Receiver: " + receiver.username)
        print("Sender: " + sender.username)
        if receiver is None:
            print(f"Skipping message with id {message.id} because receiver is None")
            continue
        try:
            decrypted_content = decrypt_message(user.private_key, message.content)
            decrypted_messages.append((sender.username, receiver.username, decrypted_content))
        except Exception as e:
            print(f"Failed to decrypt message with id {message.id}")
            print(f"Encrypted message content: {message.content}")
            print(f"Decryption key: {user.private_key}")
            print(f"Receiver: {receiver}")
            print(f"Exception: {str(e)}")

    return jsonify(decrypted_messages), 200


# message stores user id, get_user is based on username, but get_messages is trying to get user based on their id,
# which isn't how get_user works
