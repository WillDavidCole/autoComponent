## Assuming that pipenv is installed as well as python (accessible in shell)
## cd into the api directory
## issue the following commands to install package requirements and create the virtualenv

pipenv install --python 3.7
pipenv shell
pipenv install -r requirements.txt

# To run the flask api from cmd in .api/ - simply issue the following commands:
    # to start the virtual env:
        pipenv shell
    # starts the api:
        flask run 

## NOTE => the above assumes that flask, flask-restful and SQLAlchemy have been installed from 'requirements.txt'