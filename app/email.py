from threading import Thread
from flask import current_app,render_template
from flask_mail import Message
from . import mail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(recipient,subject,template,**kwargs):
    app = current_app._get_current_object()
    msg = Message("{} {}".format(app.config['ESKIMOTV_MAIL_SUBJECT_PREFIX'],subject),sender=app.config['ESKIMOTV_MAIL_SENDER'],recipients=[recipient])
    msg.body = render_template("{}.txt.j2".format(template),**kwargs)
    msg.html = render_template("{}.html.j2".format(template),**kwargs)
    thr = Thread(target=send_async_email, args=[app,msg])
    thr.start()
    return thr


def send_test_email(**kwargs):
    app = current_app._get_current_object()
    msg = Message("{} {}".format(app.config['ESKIMOTV_MAIL_SUBJECT_PREFIX'],"Test Email"),sender=app.config['ESKIMOTV_MAIL_SENDER'],recipients=["brokenmind@gmail.com"])
    msg.body = "This is a test email. Test emails should contain no information of value."
    msg.html = "This is a test email. Test emails should contain no information of value."
    send_async_email(app,msg)
