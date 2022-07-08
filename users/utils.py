import secrets
import os
from flask import current_app


def save_picture(form_picture):
    random_hex =  secrets.token_hex(8)
    _, f_text = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_text
    picture_path = os.path.join(current_app.root_path, 'static', picture_fn)
    form_picture.save(picture_path)
    return picture_fn



def send_reset_email(user):
    pass
