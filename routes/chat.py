from flask import request, session, jsonify

from app import app
from auth.middleware import require_login
from database.database import get_user, create_message, get_message
from encryption.encryption import encrypt_message, decrypt_message


@app.route('/send_message', methods=['POST'])
@require_login
def send_message():
    sender_username = session['username']
    receiver_username = request.form['receiver_username']
    content = request.form['message']

    receiver = get_user(receiver_username)
    if receiver is None:
        return 'Receiver does not exist', 400

    sender = get_user(sender_username)
    encrypted_message = encrypt_message(content, sender.public_key)

    create_message(sender_username, receiver_username, encrypted_message)
    return 'Message sent successfully', 200


@app.route('/get_messages', methods=['GET'])
@require_login
def get_messages():
    username = session['username']
    user = get_user(username)

    messages = get_message(username)

    decrypted_messages = [(message.sender, message.receiver, decrypt_message(message.content, user.private_key)) for message in messages]

    return jsonify(decrypted_messages), 200


