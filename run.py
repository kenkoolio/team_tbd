import os
from flask import Flask, render_template, flash, request, session, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
# from ibm_watson import SpeechToTextV1
# from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from spliceAndProcess import spliceAndProcess, Segment, generateDocument, create_imagetext_dictionary
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
            session['time_interval']=int(request.form['time_interval'])
            return redirect(url_for('process_file'))
    else:
        script = ["uploadscript.js"]
        return render_template("upload.html", jsscripts=script)

@app.route('/processFile')
def process_file():
    filename = session['filename']
    time_interval = session['time_interval']
    folderName = os.path.join(app.config['UPLOAD_FOLDER'],filename.replace('.', ''))
    segments = spliceAndProcess(filename, app.config['UPLOAD_FOLDER'], time_interval, folderName)
#    session['segments'] = segments
    print(segments)
    image_text = create_imagetext_dictionary(segments)
#    session['pdf_path'] = pdf_path
#    return redirect(url_for('result'))
    print(image_text)
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


        #placeholder
        return render_template("result.html", pdf=pdf_path)


# this route is just for testing purposes while I play with placeholder pdf
# we can remove it when pdf generation of our dynamic material is complete if
# we want to do this differently..
@app.route('/result')
def result():
    pdf_path = session['pdf_path']
    return render_template('result.html', pdf=pdf_path), 404

# @app.route('/getTranscription')
# def get_scribe():
#     #hardcoded for testing purposes, this will be a parameter of get_scribe and will follow the process file route
#     filename = 'clip_0.1.mp3'
#     with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as audio_file:
#         speech_recognition_results = speech_to_text.recognize(
#             audio=audio_file,
#             content_type='audio/mp3',
#             word_alternatives_threshold=0.9,
#         ).get_result()
#
#     transcript = []
#     for portion in speech_recognition_results['results']:
#         #timestamp = portion['word_alternatives'][0]['start_time']
#         text = portion['alternatives'][0]['transcript']
#         #text_data = dict({'timestamp': timestamp, 'text': text})
#         #transcript.append(text_data)
#         transcript.append(text)
#     return ('<br><br>').join(transcript)

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
