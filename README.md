# COMP3334-Group-Project

## Deployment

Set environmental variables in a `.env` file with the following:

```ini
C_NAME=<your-cloudinary-name>
C_KEY=<your-cloudinary-key>
C_SECRET=<your-cloudinary-secret>
EMAIL_HOST_USER=<your-mail-host-username>
EMAIL_HOST_PASSWORD=<your-mail-host-password>
```

1. install python virtual environment by `pip install virtualenv`.
2. create a virtual env by `python -m venv env`.
3. activate the virtual env by `source env/bin/activate`.
4. install dependencies by `pip install -r requirements.txt`.
5. init the database by `python manage.py makemigrations`.
6. confirm migration by `python manage.py migrate`.
7. run the server by `python manage.py runserver`.
8. or with https: `python manage.py runsslserver --certificate cert.pem --key key.pem`
