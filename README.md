Summer 2020 Hackathon

##Getting started: 
```bash
bash
virtualenv venv -p $(which python3) 
source ./venv/bin/activate
pip3 install --upgrade pip
pip install -r requirements.txt
```

##Running the Flask App
```bash
source ./venv/bin/activate
export FLASK_APP=run.py
python -m flask run -h 0.0.0.0 -p XXXX --reload
```

Go to: http://http://0.0.0.0/:XXXX 
