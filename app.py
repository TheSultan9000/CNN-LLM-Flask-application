# Import packages
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
import os
import sqlite3
import uuid

# As the database created is found within the instance folder, the path is saved within a variable
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'database.db')

# Flask app setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SECRET_KEY'] = ''
app.config['UPLOAD_FOLDER'] = 'static/images'
db = SQLAlchemy(app)

# The database was setup so that:
# The User table contains the admin details
# Images table contains the URL, description, and tags for the uploaded image
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(10000))
    tag = db.Column(db.String(100))
    description = db.Column(db.String(100))


@app.route("/")
def home():
    '''Returns the index.html and all Image ids, paths, tags, and descriptions from the Image table
    Expects: none
    Modified: none
    Returns: List contianing string: image path, string: tags, string: description
    '''
    photos_cleaned = sql_connection()

    return render_template("index.html", photos=photos_cleaned)


@app.route("/database_management/", methods=['GET', 'POST'])
def database_management():
    # Check if user is authenticated
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    '''Allows the user to delete images within the Image table
    Expects: Button value
    Modified: The id of the image == to the button value is removed from the Image table
    Returns: database_management.html with list contianing string: image path, string: tags, string: description
    '''
    clean_db()
    
    photos_cleaned = sql_connection()

    if request.method == 'POST':
        button_value = request.form['button']

        # Connect to the SQLite database
        conn = sqlite3.connect('instance/database.db')
        cursor = conn.cursor()

        # Execute the DELETE query
        cursor.execute("DELETE FROM Images WHERE id = ?", (button_value,))

        # Commit the transaction to save the changes
        conn.commit()

        # Close the database connection
        conn.close()

    return render_template("database_management.html", photos=photos_cleaned)


@app.route('/upload/', methods=['POST', 'GET'])
def upload():
    '''Pass the uploaded image through a pre-defined CNN and LLM
    Expects: POST request and image file path from html form
    Action: The image file is read and passed through the CNN and LLM
    Returns: List of strings: Tags from the CNN and string: description from the LLM
    '''
    if request.method == 'POST':
        if 'image' in request.files:
            
            tags, description =cnn_llm_model()

            return jsonify(result__tag=tags, result__description=description)
        
    # Render the initial template
    return render_template('upload.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    '''Authenticate the admin before being re-directed to the protected upload page
    Expects: string: username and string: password
    Action: query the database to check credentials
    Returns: string: error message or string: welcome message
    '''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(
            username=username, password=password).first()

        if user:
            # User exists
            session['user_id'] = user.id  # Store the user ID in the session
            return render_template('login.html', messsage='Welcome admin!')
        else:
            # User doesn't exist or invalid credentials
            return render_template('login.html', messsage='Invalid username or password')
    else:
        return render_template('login.html')


@app.route('/protected/', methods=['GET', 'POST'])
def protected():
    '''Pass the uploaded image through a pre-defined CNN and LLM
    Expects: POST request and image file path from html form
    Action: The image file is read and passed through the CNN and LLM
    Returns: List of strings: Tags from the CNN and string: description from the LLM
    '''
    # Check if user is authenticated
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    photos_cleaned = sql_connection()

    if request.method == 'POST':
        button_value = request.form['button']
        if button_value == 'Upload':
            if 'image' in request.files:
                
                tags, description =cnn_llm_model()

                return jsonify(result__tag=tags, result__description=description)

        elif button_value == 'Submit':
            '''Saves the image and upload the image URL, tags, and description to the Image table within the database
            Expects: POST request, button value, HTML image path, String: tags, and String: description
            Action: The image file is saved and the image URL, tags, and description are uploaded to the database
            Returns: none
            '''
            image_data = request.files['image']
            # A unique file name is given to the image with the original file extension and saved to the static folder
            if image_data.filename != '':
                filename = generate_unique_filename(image_data.filename)
                image_data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        tag_input = request.form['tag_upload']
        description_input = request.form['description_upload']

        # image URL, tags, and description are commited to the database
        new_upload = Images(photo = file_path, tag = tag_input, description = description_input)
        db.session.add(new_upload)
        db.session.commit()
        return
    # Render the initial template
    return render_template('protected.html', photos = photos_cleaned)



def sql_connection():
    '''Queries the database to extract all Image id, path, tags, and descriptions
    Expects: String: image URL, description, and tags
    Modified: The URL is extracted and static/ is removed so that it can be placed within the HTML src = {{ url_for('static', filename=photo[0]) }}
    Returns: image URL string, image description string, image tags list
    '''
    conn = sqlite3.connect('instance/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT photo, tag, description, id FROM Images")
    photos = cursor.fetchall()
    conn.close()

    sql_output = []
    for text in photos:
        link = (text[0].replace("static/",""))
        sql_output.append([link, text[1], text[2], text[3]])

    return sql_output

def cnn_llm_model():
    '''Imports and runs a CNN and LLM
    Expects: HTML Image path
    Action: Runs pre-defined CNN and LLM
    Returns: Lisft of strings: Tags from CNN and string: discription from LLM
    '''
    image = request.files['image']
    img = image.read()

    import Image_classifier
    tags_output = Image_classifier.image_classifier(img)
    
    import LLM
    description_output = LLM.image_to_text_class(img)

    return tags_output, description_output


def generate_unique_filename(filename):
    '''Assign unique file name
    Expects: String: file name
    Modifies: Extract the file extension and appends this to the end of a new unqie file name
    Returns: String: modified unique file name
    '''
    ext = filename.rsplit('.', 1)[1].lower()
    unique_name = str(uuid.uuid4().hex)
    return unique_name + '.' + ext

def clean_db():
    '''Removes any saved images which are not found within the Image table of the database
    Expects: List: Image names in database, list: image names within static folder
    Modifies: Any images in the folder which are not in the database are removed
    Returns: none.
    '''
    photos = sql_connection()

    files = []
    for photo in photos:
        link = (photo[0].replace("images/",""))
        files.append(link)

    files.append("Full_logo-1.png")

    img_dir = "static/images"
    saved_images = os.listdir(img_dir)

    for image in saved_images:
        if image not in files:
            os.remove(os.path.join(img_dir, image))


if __name__ == "__main__":
    app.run(debug=True)
