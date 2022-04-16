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

1. install python virtual environment.
   ```sh
   pip install virtualenv
   ```
1. Create and activate a virtual environment, and then install all dependencies
   ```sh
   python -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```
1. Initialize Django
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```
2. run the server by any one from the following.
   ```sh
   python manage.py runserver
   python manage.py runsslserver --certificate cert.pem --key key.pem
   ```
