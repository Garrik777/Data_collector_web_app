from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from Include.db_config import Config
from Include.send_email import send_email
from sqlalchemy.sql import func
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Data(db.Model):
    __tablename__ = "data"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    height = db.Column(db.Integer)

    def __init__(self, username, height):
        self.username = username
        self.height = height

    def __repr__(self):
        return f'{self.username}:{self.height}'


@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')


@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        email = request.form['email']
        height = request.form['height']
        if not db.session.query(Data).filter(Data.username == email).count():
            data = Data(email, height)
            db.session.add(data)
            db.session.commit()
            av_height = db.session.query(func.avg(Data.height)).scalar()
            av_height = round(av_height, 1)
            count = db.session.query(Data.height).count()
            send_email(email, av_height, count)
            return render_template('success.html', message='Thank you for submission. You will recieve e-mail '
                                                           'shortly<br>')
    return render_template('index.html', error='Email already exists. Enter another email<br>')

@app.route('/success_file', methods=['POST'])
def success_file():
    global file
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('index.html', btn='download.html')

@app.route('/download')
def download():
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], file.filename), attachment_filename="dowloaded.txt",
                     as_attachment=True)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
