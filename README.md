# CNN and LLM Flask application

...
## A Flask application to classify and describe images before upload

...
### Description:
This training exercises has resulted in an app which allows the admin to:
* Upload an image
* Run a CNN and LMM to generate tags and a description of the uploaded image
* Select the desired tags and description before submitting the infromation to a sqlight3 server
* View all images, descriptions, and tags within the sqlight3 database and delete items
* View uplaoded images on the index

Although non-admin users cannot submit images, a parallel upload html template was created so that anyone can experience the CNN and LLM without actually submitting an image:
* CNN: has been trained on images of the English countryside and will output 'Animal', 'building', and 'Nature' (Precision: 1, Recall: 0.9, Accuracy: 0.6)
* LLM: https://huggingface.co/nlpconnect/vit-gpt2-image-captioning

![Alt text](<example_images/Screenshot 2023-07-26 at 08.18.48.png>)
![Alt text](<example_images/Screenshot 2023-07-26 at 08.19.05.png>)
![Alt text](<example_images/Screenshot 2023-07-26 at 08.53.34.png>)
...
### Directory
* root folder
    * app.py - this is the application which uses the Flask framework
    * CNN.h5 - this is the CNN which is used within Image_flassified.py to generate tags
    * LLM.py - this is the LLM which is used to generate descriptions
* instances
    * database.db - contains the admin login details and images
* static
    * images - image uploads (the files paths for these images are stored within the sqlight3 database)
    * styles - CSS and Javascript files 
* templates
    * HTML files used in the app.py Flask framework

...
### Installation and use:
* Once the app has been cloned, ensure the dependencies have been installed below.
* Ensure all the files are kept within the same direcotry structure and run the app.py file within the python termianl or console.

It is important to note that for security:
* The secret key has been removed (within the app.py setup)
* The admin details have been chnaged to username: admin and password: password
You must change these if you wish to use the app in a live environment. To change the admin details:
To delete current admin details:
```console
sqlite3 instance/database.db

DELETE FROM User WHERE id = 1;
```

To create new admin details:
```python
from app import app, db, User
with app.app_context():
db.session.add(User(username="admin", password="password"))
db.session.commit()
```

To setup secret key:
```python
app.config['SECRET_KEY'] =
```

Tamplates-
* base- this is the base template which every other template is extended from. Themain components are the global styling, logo and navigation bar.
    * The about link can be modified for own use.
* index- the home page where the image are seen
    * Tags and description are found within a light box
* upload- this page is meant for non-admon users, so that they can experience the CNN and LLM (the submit button simply refreshes the page)
* login- this is for the admin to access protected pages
    * protected- this mirrors the upload page but the submit button will upload the image to the server and display on the index page
    * database_management- a way to visualise all the image sin the database and delete unwanted images.

...
### Dependencies
Created using python version Python 3.10.9
```python
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
import os
import sqlite3
import uuid
import numpy as np
import tensorflow as tf
from keras.models import load_model
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
```

...
### Contributions
Although contributions and comments are always welcome, please be aware that is project was used as a learning excersise and is not being activally maintained.
