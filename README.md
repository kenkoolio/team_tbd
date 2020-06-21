Summer 2020 BeaverHacks

# :memo: Scribe

Scribe is an accessability-focused application that is meant to help students, especially deaf and hard-of-hearing students, to obtain accurate and clear transcriptions of lecture recordings.

A student or professor can easily upload a locally downloaded `mp4` file, or provide a web link to a video hosted online by YouTube or the user's school.  If video captions are available as a part of the video uploaded, those will be used.  Otherwise, a video transcription will be generated.  A `pdf` will be produced that includes video transcription text interlaced with images of the uploaded video at the appropriate timestamp.  The user can then download, print, or e-mail the resulting `pdf`.

Additional features include language translation to a language of the user's choosing, and user-editing of the resulting transcription to ensure the best accuracy possible in the final transcription pdf.

Scribe also has many other possible uses for thoroughly documenting any type of lecture or presentation.

![Scribe Homepage](https://class-scribe.herokuapp.com/)

## :hammer: Scribe is built with:
- [Heroku](https://www.heroku.com/)
- [IBM Watson](https://cloud.ibm.com/developer/watson/dashboard)
- [MoviePy](https://pypi.org/project/moviepy/)
- [SendGrid](https://sendgrid.com/)
- [googletrans](https://pypi.org/project/googletrans/)
- [FPDF](https://pyfpdf.readthedocs.io/en/latest/)
- [Python3](https://www.python.org/downloads/)
- [jQuery](https://jquery.com/)
- [Bootstrap](https://getbootstrap.com/)
- [MDB](https://mdbootstrap.com/)

## 🤓 Authors
- [Mae LaPresta](https://github.com/mlapresta)
- [Noah Johnston](https://github.com/NDJ-1701)
- [Ken Nguyen](https://github.com/kenkoolio)
- [Elizabeth Tackett](https://github.com/emtackett)

## :earth_americas: View on the web:
[Scribe](https://class-scribe.herokuapp.com/) is hosted by Heroku.

## 💻 Work locally:
- Clone the repository: `git clone https://github.com/kenkoolio/team_tbd.git`
- From the command line, navigate into the `team_tbd` directory.
- Execute the following commands on the command line:

### Set up
```bash
virtualenv venv -p $(which python3)
source ./venv/bin/activate
pip3 install --upgrade pip
pip install -r requirements.txt
export API_KEY=[IBM_WATSON_API_KEY]
export API_URL=[IBM_WATSON_API_URL]
export SESSION_KEY=[SESSION KEY]
export SENDGRID_API_KEY=[SENDGRID_API_KEY]

# if you're on mac OS High Sierra, you may need the following to run
# the script locally
export OBJ_DISABLE_INITIALIZE_FORK_SAFETY=yes
```
- Note that you will need to obtain an `IBM_WATSON_API_KEY` for `IBM_WATSON_API_URL` from [Cloud IBM Watson](https://cloud.ibm.com/docs/speech-to-text?topic=speech-to-text-languageCreate), as well as a `SENDGRID_API_KEY` from [SendGrid](https://sendgrid.com/).
- The `SESSION_KEY` environment variable can be anything.

### Running the Flask App
```bash
source ./venv/bin/activate
export FLASK_APP=run.py
python -m flask run -h 0.0.0.0 -p XXXX --reload
```
- Visit http://0.0.0.0/:XXXX in your browser
