# Smart P2P marketplace

A web application built on django an application where users can upload images of products that are up for sale. The application has the functionality of categorizing the products. It uses clarifai to auto categorize the images. It also has the following features:

* The users can register themselves on the website, and after a successful sign up a welcome email is sent to the user.
* The users can log in the website to view the feed which is visible to every user.
* Add post option which uses cloudinary API to upload image on the cloud after storing locally.
* Options to like and comment on individual posts.
* On each like and comment the owner of the post gets an email notification.
* The user can log out

## APIs Used

* cloudinary
* clarifai
* sendgrid

## Installation

To run this project on your local computer make sure you have installed python,pip,virtualenv and easy_install on your system.

After that clone this repository and set up your own virtual environment.

Install the dependencies using:

> pip install -r requirements.txt

In settings.py, set up the following variables

```python
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = '<YOUR_USERNAME>'
EMAIL_HOST_PASSWORD = '<YOUR_PASSWORD>'
DEFAULT_FROM_EMAIL = 'webmaster@localhost'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

Create a KEYS.py with the following variables:

```python
clarifai_key = '<YOUR_CLARIFAI_KEY>'
cloudinary_api_key = '<YOUR_CLOUDINARY_KEY>'
cloudinary_secret  = '<YOUR_CLOUDINARY_AUTH_SECRET>'
cloudinary_cloud_name = '<YOUR_CLOUD_NAME>'
```

Go to the root directory(make sure you have your virtual environment enabled) and run:

> python manage.py runserver

## Screenshots

Here is the website in action:

[![solarized dualmode](https://github.com/sarthak625/SmartP2PMarketPlace/blob/master/screenshots/sm_sc_1.png)](#features)

[![solarized dualmode](https://github.com/sarthak625/SmartP2PMarketPlace/blob/master/screenshots/sm_sc_2.png)](#features)

[![solarized dualmode](https://github.com/sarthak625/SmartP2PMarketPlace/blob/master/screenshots/sm_sc_3.png)](#features)

[![solarized dualmode](https://github.com/sarthak625/SmartP2PMarketPlace/blob/master/screenshots/sm_sc_4.png)](#features)

[![solarized dualmode](https://github.com/sarthak625/SmartP2PMarketPlace/blob/master/screenshots/sm_sc_5.png)](#features)
