# COMP3334-Group-Project

## Deployment

1. install python virtual environment by `pip install virtualenv`.
2. create a virtual env by `python -m venv env`.
3. activate the virtual env by `source env/bin/activate`.
4. install dependencies by `pip install -r requirements.txt`.
5. init the database by `python manage.py makemigrations marketapp`.
6. confirm migration by `python manage.py migrate`.
7. run the server by `python manage.py runserver`.