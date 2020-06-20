import os
import base64
from flask import Flask, render_template, flash, request, session, redirect, url_for
from werkzeug.utils import secure_filename
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)
from spliceAndProcess import spliceAndProcess
import json


UPLOAD_FOLDER='./static/media'
ALLOWED_EXTENSIONS = {'wav', 'mp4', 'avi'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.environ.get('SESSION_KEY')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        print(request)
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.mkdir(app.config['UPLOAD_FOLDER'])

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            session['filename'] = filename
            return redirect(url_for('process_file'))
    else:
        return render_template("upload.html")

@app.route('/processFile')
def process_file():
    filename = session['filename']
    folderName = os.path.join(app.config['UPLOAD_FOLDER'],filename.replace('.', ''))
    pdf_path = spliceAndProcess(filename, app.config['UPLOAD_FOLDER'], 60, folderName)

    session['pdf_path'] = pdf_path
    return redirect(url_for('result'))

@app.route('/result')
def result():
    pdf_path = session['pdf_path']
    return render_template('result.html', pdf=pdf_path)

@app.route('/send', methods=['POST'])
def send():
    receiver = request.form['email-input']
    pdf_path = request.form['pdf'][1:]
    pdf_filename = pdf_path.split('static/pdf/')[-1]

    message = Mail(
        from_email='class-scribe@mail.com',
        to_emails=receiver,
        subject='Class Scribe: Your notes',
        html_content="<p>Class Scribe has sent you notes!  View the attached PDF for audio transcription and visual aides.</p><br><br><p>Class Scribe</p>")

    with open(pdf_path, 'rb') as f:
        data = f.read()
        f.close()
    encoded_file = base64.b64encode(data).decode()

    attached_file = Attachment(
        FileContent(encoded_file),
        FileName(pdf_filename),
        FileType('application/pdf'),
        Disposition('attachment')
    )
    message.attachment = attached_file

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
    except Exception as e:
        print(e)

    flash('Email sent! You may upload another video file now.')
    return redirect(url_for('upload'))


@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def not_found(error):
    return render_template('500.html'), 404

if __name__ == '__main__':
    app.run()
