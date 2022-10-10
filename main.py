from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///swift.db'
app.config['SQLALCHEMY_BINDS'] = {
    'two': 'sqlite:///carbros.db'
}
db = SQLAlchemy(app)

conn = sqlite3.connect('carbros.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

class deals(db.Model):
    __bind_key__ = 'two'
    car = db.Column(db.String, unique=True)
    year = db.Column(db.Integer, unique=False)
    owner = db.Column(db.String, primary_key=True)
    image = db.Column(db.String, unique=False)
    description = db.Column(db.String, unique=False)


db.create_all()


class Car(db.Model):
    email = db.Column(db.String, primary_key=True)
    phone = db.Column(db.Integer, unique=False)
    password = db.Column(db.String, unique=False)



db.create_all()


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        car = Car(email=email, phone=phone, password=generate_password_hash(password))
        db.session.add(car)
        db.session.commit()
    return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email_l = request.form.get('email')
        password_l = request.form.get('password')
        x = Car.query.filter_by(email=email_l).first()
        password_r = x.password
        email_r = x.email
        if email_r == email_l:
            if check_password_hash(pwhash=password_r, password=password_l):
                return redirect(url_for('buy'))
    return render_template('login.html')


@app.route('/buy')
def buy():
    conn = sqlite3.connect('carbros.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    year = 100000000000
    sql = ("""SELECT * FROM deals WHERE year <= {};""").format(year)
    cur.execute(sql)
    result = cur.fetchall()
    return render_template('buy.html', x=result)


@app.route('/sell',methods=['POST', 'GET'])
def sell():
    if request.method == 'POST':
        name = request.form.get('name')
        car = request.form.get('car')
        year = request.form.get('phone')
        image = request.form.get('image')
        description = request.form.get('des')
        deal = deals(car=car,year=year,owner=name, image=image, description=description)
        db.session.add(deal)
        db.session.commit()
    return render_template('sell.html')

@app.route('/remove',methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        image = request.form.get('link')
        car = deals.query.filter_by(image=image).first()
        db.session.delete(car)
        db.session.commit()
    return render_template('remove.html')
if __name__ == '__main__':
    app.run(debug=True)
