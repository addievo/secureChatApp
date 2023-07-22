from datetime import datetime
from flask import request, session, jsonify
from app import app
from auth.middleware import require_login
from database.database import get_user, create_message, get_messages_for_user
from encryption.encryption import encrypt_message, decrypt_message

current_time = datetime.now()


@app.route('/send_message', methods=['POST'])
@require_login
def send_message():
    sender_username = session['username']
    receiver_username = request.form['receiver_username']
    content = request.form['message']

    sender = get_user(sender_username)
    receiver = get_user(receiver_username)


    if receiver is None:
        return 'Receiver does not exist', 400


    receiver_public_key = receiver.public_key


    encrypted_message = encrypt_message(receiver_public_key, content)

    create_message(sender.id, receiver.id, encrypted_message, current_time)
    return 'Message sent successfully', 200


@app.route('/get_messages', methods=['GET'])
@require_login
def get_messages():
    username = session['username']
    user = get_user(username)

    messages = get_messages_for_user(user.id)

    decrypted_messages = []
    for message in messages:
        try:
            decrypted_content = decrypt_message(user.private_key, message.content)
            decrypted_messages.append((message.sender, message.receiver, decrypted_content))
        except Exception as e:
            print(f"Failed to decrypt message with id {message.id}")
            print(f"Encrypted message content: {message.content}")
            print(f"Decryption key: {user.private_key}")
            print(f"Receiver: {message.receiver}")
            print(f"Exception: {str(e)}")

    return jsonify(decrypted_messages), 200
