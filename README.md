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
3. Initialize the Django database schema.
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Save environmental variables into a `.env` file:

   ```ini
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

5. Run the server on localhost.
   ```sh
   python manage.py runserver              # run the server in http
   python manage.py runsslserver \         # run the server in https
   --certificate cert.pem --key key.pem    #   with local certificate
   ```

By opening the URL shown in the console after running the server (maybe [http://127.0.0.1:8000](http://127.0.0.1:8000) or [https://127.0.0.1:8000](https://127.0.0.1:8000)) with browser, a welcome page should show up, which indicates completion of deployment.
