from datetime import datetime
from flask import request, session, jsonify, render_template
from auth.middleware import require_login
from database.database import get_user, create_message, get_messages_for_user_and_partner, get_conversations_for_user
from encryption.encryption import encrypt_message, decrypt_message
from flask import Blueprint
from flask import json

current_time = datetime.utcnow()

bp = Blueprint('chat', __name__)

@bp.route('/get_conversations', methods=['GET'])
@require_login
def get_conversations():
    username = session['username']
    user = get_user(username)
    conversations = get_conversations_for_user(user.id)
    return jsonify(conversations), 200

@bp.route('/send_message', methods=['POST'])
@require_login
def send_message():
    data = request.get_json()
    sender_username = session['username']
    receiver_username = data['receiver_username']
    content = data['message']

    sender = get_user(sender_username)
    receiver = get_user(receiver_username)

    if receiver is None:
        return jsonify({"error": "Receiver does not exist"}), 400

    #encrypting message for receiver using receiver's public key
    receiver_public_key = receiver.public_key
    encrypted_message_for_receiver = encrypt_message(receiver_public_key, content)

    #encrypting message for sender using sender's public key
    sender_public_key = sender.public_key
    encrypted_message_for_sender = encrypt_message(sender_public_key, content)

    #store both encrypted messages in database
    create_message(sender.id, receiver.id, encrypted_message_for_sender, encrypted_message_for_receiver, current_time)

    return jsonify({"success": "Message sent"}), 200


@bp.route('/get_messages', methods=['GET'])
@require_login
def get_messages():
    username = session['username']
    partner_username = request.args.get('username')
    user = get_user(username)
    partner = get_user(partner_username)


    if partner is None:
        return jsonify({"error": "Partner does not exist"}), 400

    messages = get_messages_for_user_and_partner(user.id, partner.id)

    decrypted_messages = []
    for message in messages:
        sender = get_user(None, message.sender_id)
        receiver = get_user(None, message.receiver_id)
        if receiver is None:
            print(f"Skipping message with id {message.id} because receiver is None")
            continue

        # Decrypt the message content based on who the user is in the conversation
        if user.id == sender.id:
            decrypted_content = decrypt_message(user.private_key, message.content_for_sender)
        elif user.id == receiver.id:
            decrypted_content = decrypt_message(user.private_key, message.content_for_receiver)

        decrypted_messages.append((sender.username, receiver.username, decrypted_content, message.timestamp))

    return jsonify(decrypted_messages), 200