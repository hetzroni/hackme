You can try out the server here: https://hetzroni-hackme.herokuapp.com/

To setup the server locally, run the following commands:

    git clone https://github.com/hetzroni/hackme.git
    cd hackme
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

In order to run the server:

    FLASK_ENV=development flask run

In order to run the tests:

	pytest
