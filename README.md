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
   After step 4, open a Web browser and go to “/admin/” on your local domain – e.g., http://127.0.0.1:8000/admin/. You should see the admin’s login screen.
   
5. run the server by any one from the following.
   ```sh
   python manage.py runserver              # run the server in http
   python manage.py runsslserver \         # run the server in https
   --certificate cert.pem --key key.pem    #   with local certificate
   ```

By opening the URL shown in the console after running the server (maybe [http://127.0.0.1:8000](http://127.0.0.1:8000) or [https://127.0.0.1:8000](https://127.0.0.1:8000)) with browser, a welcome page should show up, which indicates completion of deployment.
