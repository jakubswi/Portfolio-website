# -*- coding: utf-8 -*-
from email.mime.text import MIMEText
from email.header import Header
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
import smtplib
import os
import resend

app = Flask(__name__)
Bootstrap5(app)
MAIL_ADDRESS = os.environ.get("EMAIL_ADDRES")

@app.route('/')
def main_page():
    return render_template("index.html")

resend.api_key = os.environ.get("RESEND_API_KEY")

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
    response = resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": MAIL_ADDRESS,
        "subject": 'New Message',
        "html": f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}",
    })


if __name__ == "__main__":
    app.run(debug=False)
