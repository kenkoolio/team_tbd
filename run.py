import os
from flask import Flask, render_template, flash, request, session, redirect, url_for, jsonify
from spliceAndProcess import spliceAndProcess, Segment, generateDocument, create_imagetext_dictionary
import base64
from werkzeug.utils import secure_filename
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)
from downloadVideoURL import download_video
from multiprocessing import Process
import json
import time


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
            session['time_interval']=int(request.form['time_interval'])
            session['translation']=request.form['translation']
            return redirect(url_for('process_file'))
    else:
        script = ["uploadscript.js"]
        return render_template("upload.html", jsscripts=script)


@app.route('/upload-from-url', methods=['POST'])
def upload_from_url():
    try:
        video_url = request.form["video_url"]
        if ('youtube.com' in video_url) or ('youtu.be' in video_url) or ('oregonstate.edu' in video_url):
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.mkdir(app.config['UPLOAD_FOLDER'])

            session['filename'] = download_video(video_url, app.config['UPLOAD_FOLDER'], request.form['translation'])
            session['time_interval'] = int(request.form["time_interval"])
            session['translation']=request.form['translation']
            return redirect(url_for('process_file'))
        else:
            flash('Incorrect Video URL')
            return redirect('upload')
    except Exception as e:
        print(f'Error: /upload-from-url route failed: {e}')
        return redirect('index')


@app.route('/processFile')
def process_file():
    filename = session['filename']
    time_interval = session['time_interval']
    folderName = os.path.join(app.config['UPLOAD_FOLDER'],filename.replace('.', ''))
    filepath = folderName + '/' + filename + '.json'
    #segments = spliceAndProcess(filename, app.config['UPLOAD_FOLDER'], time_interval, folderName)
#    print(segments)
#    image_text = create_imagetext_dictionary(segments)
#    session['pdf_path'] = pdf_path
#    return redirect(url_for('result'))
#    print(image_text)
    translation=session['translation']
    global p
    p = Process(target=detachedProcessFile, args=(filename, folderName, time_interval, filepath, translation))
    p.start()
    script = ['processscript.js']
#    return render_template("editTranscription.html", image_text=image_text)
    return render_template("processing.html", filepath = filepath, jsscripts = script)

@app.route('/processStatus', methods=['POST'])
def get_process_status():
    if request.method == 'POST':
        filepath = request.get_json(force=True)['filepath']
        response = {'complete': 0}

        # if the file exists, then the detachedProcessFile() function has completed
        if os.path.exists(filepath):
            response['complete'] = 1

        return jsonify(response)

@app.route('/processComplete', methods=['POST'])
def process_complete():
    if request.method == 'POST':
        filepath = request.get_json(force=True)['filepath']
        #get the saved to file image_text dictionary,
        #this was done in detachedProcessFile
        f = open(filepath)
        image_text = json.load(f)
        return render_template("editTranscription.html", image_text=image_text)

@app.route('/updateTranscription', methods=['POST'])
def update_transcription():
    if request.method == 'POST':
        #print (request.get_json(force=True))
        #print(request.values)
        updated_text = request.form

        segments = []
        for index, key in enumerate(updated_text):
            segments.append(Segment(0,0))
            segments[index].imagePath = key
            segments[index].text = updated_text[key]
            print(segments[index])

        filename = session['filename']
        folderName = os.path.join(app.config['UPLOAD_FOLDER'],filename.replace('.', ''))
        pdf_path = generateDocument(filename, segments, folderName)

        return render_template("result.html", pdf=pdf_path)


@app.route('/result')
def result():
    pdf_path = session['pdf_path']
    return render_template('result.html', pdf=pdf_path)

@app.route('/send', methods=['POST'])
def send():
    receiver = request.form['email-input']
    pdf_path = './' + request.form['pdf'][1:]
    pdf_filename = pdf_path.split('static/media/')[-1]
    print(pdf_path)
    print(pdf_filename)
    message = Mail(
        from_email='class-scribe@mail.com',
        to_emails=receiver,
        subject='Scribe: Your notes.',
        html_content="<p>Scribe has sent you notes!  View the attached PDF for audio transcription and visual aides.</p><br><br><p>Class Scribe</p>")

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


#This is run separately and saves the image_text dictionary in a file
def detachedProcessFile(filename, folderName, time_interval, filepath, language):
    segments = spliceAndProcess(filename, app.config['UPLOAD_FOLDER'], time_interval, folderName, language)
    image_text = create_imagetext_dictionary(segments)
    with open(filepath, 'w') as f:
        json.dump(image_text, f)

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
