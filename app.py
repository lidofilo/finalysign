# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv
import sqlite3

# تحميل متغيرات البيئة
load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"

# إعدادات البريد الإلكتروني - Outlook
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = ("FinalySign", os.getenv("MAIL_USERNAME"))



def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


mail = Mail(app)


# الصفحة الرئيسية
@app.route('/')
def home():
    return render_template('index.html', title="FinalySign - الخدمات المالية والتحليل")


# من نحن
@app.route('/about')
def about():
    return render_template('about.html', title="من نحن - FinalySign")


# الخدمات
@app.route('/services')
def services():
    return render_template('services.html', title="خدماتنا - FinalySign")


# أعمالنا
@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', title="أعمالنا - FinalySign")


# اتصل بنا
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        msg = Message(
    subject=f"📩 رسالة جديدة من {name}",
    recipients=['w.elfil.pyramids@gmail.com'],  # مؤقتًا للتجربة
    body=f"""
الاسم: {name}
البريد: {email}

الرسالة:
{message}
"""
)

        try:
            mail.send(msg)
            flash("✅ تم إرسال الرسالة بنجاح! سنتواصل معك قريبًا.", "success")
        except Exception as e:
            print("❌ خطأ أثناء الإرسال:", e)
            flash("حدث خطأ أثناء إرسال الرسالة. حاول لاحقًا.", "danger")

        return redirect(url_for('contact'))

    return render_template('contact.html', title="اتصل بنا - FinalySign")

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    keyword = ""

    if request.method == 'POST':
        keyword = request.form.get('keyword')

        conn = get_db_connection()
        results = conn.execute(
            "SELECT * FROM records WHERE title LIKE ? OR description LIKE ?",
            (f"%{keyword}%", f"%{keyword}%")
        ).fetchall()
        conn.close()

    return render_template('search.html', results=results, keyword=keyword)



if __name__ == "__main__":
    app.run(debug=True)
