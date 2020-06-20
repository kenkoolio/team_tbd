import os
from flask import Flask, render_template, flash, request, session, redirect, url_for
from werkzeug.utils import secure_filename
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
# from ibm_watson import SpeechToTextV1
# from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from spliceAndProcess import spliceAndProcess
import json


UPLOAD_FOLDER='./static/media'
ALLOWED_EXTENSIONS = {'wav', 'mp4', 'avi'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.environ.get('SESSION_KEY')

# authenticator = IAMAuthenticator(os.environ.get('API_KEY'))
# speech_to_text = SpeechToTextV1(
#     authenticator=authenticator
# )
# speech_to_text.set_service_url(os.environ.get('API_URL'))
# speech_to_text.set_disable_ssl_verification(True)


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

@app.route('/send', methods=['GET', 'POST'])
def send():
    message = Mail(
        from_email='class-scribe@mail.com',
        to_emails='emctackett@gmail.com',
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

    return 'hello'
    
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
