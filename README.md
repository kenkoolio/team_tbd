Summer 2020 Hackathon

##Getting started:
```bash
bash
virtualenv venv -p $(which python3)
source ./venv/bin/activate
pip3 install --upgrade pip
pip install -r requirements.txt
export API_KEY=[API KEY]
export API_URL=[API URL]
export SESSION_KEY=[SESSION KEY]
export SENDGRID_API_KEY=[SENDGRID_API_KEY]
```

##Running the Flask App
```bash
bash
source ./venv/bin/activate
export FLASK_APP=run.py
python -m flask run -h 0.0.0.0 -p XXXX --reload
```

Go to: http://0.0.0.0/:XXXX
