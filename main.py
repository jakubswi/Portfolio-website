# -*- coding: utf-8 -*-
from email.mime.text import MIMEText
from email.header import Header
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
import smtplib
import os

app = Flask(__name__)
Bootstrap5(app)
MAIL_ADDRESS = os.environ.get("EMAIL_KEY")
MAIL_APP_PW = os.environ.get("PASSWORD_KEY")
@app.route('/')
def main_page():
    return render_template("index.html")


@app.route('/resume')
def resume():
    return render_template("resume.html")


@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    email_message = MIMEText(email_message, 'plain', 'utf-8')
    email_message['From'] = MAIL_ADDRESS
    email_message['To'] = MAIL_ADDRESS
    email_message['Subject'] = Header('New Message', 'utf-8')
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MAIL_ADDRESS, MAIL_APP_PW)
        connection.sendmail(MAIL_ADDRESS, MAIL_ADDRESS, email_message.as_string())


if __name__ == "__main__":
    app.run(debug=False)
