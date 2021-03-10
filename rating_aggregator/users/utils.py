import os
from flask import url_for, current_app
from flask_mail import Message
from rating_aggregator import mail

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Request Reset for Password',
                    sender='noreply@gmail.com', 
                    recipients=[user.email])
    msg.body = f'''To reset your password, please visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you didn't make this request, then please ignore this email, no changes will be made!
'''
    mail.send(msg)