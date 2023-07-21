from flask import request, session
from database.database import get_user, create_user
from werkzeug.security import generate_password_hash
from app import app

@app.route('/update_profile', methods=['POST'])
def update_profile():
    username = session['username']
    new_username = request.form.get('new_username')
    new_password = request.form.get('new_password')
    new_avatar = request.files.get('new_avatar')
    new_status = request.form.get('new_status')

    #validation testing
    if new_username and get_user(new_username):
        return 'Username already taken', 400

    #test password strength

    if new_password and len(new_password) < 8:
        return 'Password too short', 400

    #testing avatar

    valid_image_extensions = ['jpg', 'jpeg', 'png', 'gif']
    if new_avatar and '.' in new_avatar.filename and new_avatar.filename.rsplit('.', 1)[1].lower() not in valid_image_extensions:
        return 'Invalid image', 400

    #testing status

