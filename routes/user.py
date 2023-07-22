import os
import secrets

from flask import current_app, Blueprint
from flask import request, session
from werkzeug.security import generate_password_hash

from database.database import get_user, update_user
bp = Blueprint('user', __name__)


def save_avatar(avatar):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(avatar.filename)
    filename = random_hex + file_extension

    # create file path

    file_path = os.path.join(current_app.root_path, 'static/avatars', filename)

    # save avatar to file path

    avatar.save(file_path)

    return filename


@bp.route('/update_profile', methods=['POST'])
def update_profile():
    username = session['username']
    new_username = request.form.get('new_username')
    new_password = request.form.get('new_password')
    new_avatar = request.files.get('new_avatar')
    new_status = request.form.get('new_status')

    # validation testing
    if new_username and get_user(new_username):
        return 'Username already taken', 400

    # test password strength

    if new_password and len(new_password) < 8:
        return 'Password too short', 400

    # testing avatar

    valid_image_extensions = ['jpg', 'jpeg', 'png', 'gif']
    if new_avatar and '.' in new_avatar.filename and new_avatar.filename.rsplit('.', 1)[
        1].lower() not in valid_image_extensions:
        return 'Invalid image', 400

    # testing status

    if new_status and len(new_status) > 500:
        return 'Status too long', 400

    password_hash = generate_password_hash(new_password) if new_password else None

    avatar_filename = save_avatar(new_avatar) if new_avatar else None

    update_user(username, new_username, password_hash, avatar_filename, new_status)

    return 'Profile updated successfully', 200
