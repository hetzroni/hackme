You can try out the server here: https://hetzroni-hackme.herokuapp.com/

In order to run the server locally, first pull the repo. Then run the following commands:

    git clone https://github.com/hetzroni/hackme.git
    cd hackme
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    FLASK_ENV=development flask run
