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
2. Create and activate a virtual environment, and then install all dependencies
   ```sh
   python -m venv env
   source env/bin/activate # (This is just for macos)
   pip install -r requirements.txt
   ```
3. Initialize Django
   ```sh
   python manage.py makemigrations
   python manage.py makemigrations marketapp
   python manage.py migrate
   ```
4. Creating an admin user

   First we’ll need to create a user who can login to the admin site. Run the following command:
   ```sh
   python manage.py createsuperuser
   ```
   Enter your desired username and press enter.
   ```sh
   Username: admin
   ```
   You will then be prompted for your desired email address:
   ```sh
   Email address: admin@example.com
   ```
   The final step is to enter your password. You will be asked to enter your password twice, the second time as a confirmation of the first.
   ```sh
   Password: **********
   Password (again): *********
   Superuser created successfully.
   ```
   After step 4, open a Web browser and go to “/admin/” on your local domain – e.g., http://127.0.0.1:8000/admin/. You should see the admin’s login screen.
5. run the server by any one from the following.
   ```sh
   python manage.py runserver
   python manage.py runsslserver --certificate cert.pem --key key.pem
   ```
