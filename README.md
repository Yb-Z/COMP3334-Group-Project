# COMP3334-Group-Project

## Deployment

The requirements of the project on its hosting platform is shown in Table below. Make sure the requirements are met before proceeding to deploy the project.

|   Type   |                  Minimum                  |               Recommended                |
| :------: | :---------------------------------------: | :--------------------------------------: |
|    OS    | Windows 10; MacOS 10.9; Linux 4.0(kernel) | Windows 11; MacOS 13; Linux 5.17(kernel) |
| Software |                Python 3.8                 |             Python 3.9, 3.10             |

1. Make sure having python libarary `virtualenv` installed, or install with `pip install virtualenv`. 
2. Initialize a new virtualenv and install all dependencies.
   ```sh
   python -m venv env                      # create virtual environment
   source env/bin/activate                 # activate virtual environment
   pip install -r requirements.txt         # install all dependencies
   ```
2. Create and activate a virtual environment, and then install all dependencies
   ```sh
   python -m venv env
   source env/bin/activate # For windows: run .\env\Scripts\activate
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
   After step 8, open a Web browser and go to “/admin/” on your local domain – e.g., https://127.0.0.1:8000/admin/. You should see the admin’s login screen.
5. Save environmental variables into a .env file:
   ```sh
   # Cloudinary api configurations (available after registration),
   # see https://cloudinary.com/
   C_NAME = ""
   C_KEY = ""
   C_SECRET = ""
   # email backend configurations
   # send to console: "django.core.mail.backends.console.EmailBackend"
   # send to mailbox: "django.core.mail.backends.smtp.EmailBackend"
   EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
   # A mail account as host for sending emails
   EMAIL_HOST = ""
   EMAIL_HOST_USER = ""
   EMAIL_HOST_PASSWORD = ""
   # Django Secret key
   SECRET_KEY = ""
   ```
6. make locally-trusted development certificates for https. 

   you may use this tool: [mkcert](https://github.com/FiloSottile/mkcert), to generate the certificate and the key.
7. run the server by any one from the following.
   ```sh
   python manage.py runserver              
   # run the server in http
   python manage.py runsslserver --certificate cert.pem --key key.pem          
   # run the server in https with local certificate generated from 6. (Recommended)
   ```
By opening the URL shown in the console after running the server (maybe [http://127.0.0.1:8000](http://127.0.0.1:8000) or [https://127.0.0.1:8000](https://127.0.0.1:8000)) with browser, a welcome page should show up, which indicates completion of deployment.
