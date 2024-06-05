import os
import tensorflow as tf
from flask import Flask, request, render_template, jsonify, g
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.xception import preprocess_input
import numpy as np
import sqlite3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
app.config['DATABASE'] = 'app/database.db'  # Define the database path

# Load the trained model
model = tf.keras.models.load_model('model/model.keras')

# Define the class labels (make sure these match your training data)
class_names = ['Topwear', 'Shoes', 'Bags', 'Bottomwear', 'Watches', 'Innerwear', 'Jewellery', 'Eyewear', 'Fragrance', 'Sandal', 'Wallets',
                'Flip Flops', 'Belts', 'Socks', 'Lips', 'Dress', 'Loungewear and Nightwear', 'Saree', 'Nails', 'Makeup', 'Headwear', 'Ties',
                  'Accessories', 'Scarves', 'Cufflinks', 'Apparel Set', 'Free Gifts', 'Stoles', 'Skin Care', 'Skin', 'Eyes', 'Mufflers',
                    'Shoe Accessories', 'Sports Equipment', 'Gloves', 'Hair', 'Bath and Body']

# Database setup
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Create the images table if it doesn't exist
with app.app_context():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            class TEXT,
            probability REAL
        )
    ''')
    db.commit()

# Define a function to preprocess the image
def preprocess_image(img):
    img = img.resize((120, 160))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img

# Define a route for the home page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Define a route for batch processing
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'files[]' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        files = request.files.getlist('files[]')
        predictions = []

        for file in files:
            # Save the file to the uploads folder
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Load and preprocess the image
            img = image.load_img(file_path, target_size=(120, 160))
            img = preprocess_image(img)

            # Make the prediction
            prediction = model.predict(img)
            class_index = np.argmax(prediction)
            class_label = class_names[class_index]
            probability = prediction[0][class_index]

            # Save the prediction to the database
            with app.app_context():
                db = get_db()
                cursor = db.cursor()
                cursor.execute('''
                    INSERT INTO images (filename, class, probability)
                    VALUES (?, ?, ?)
                ''', (file.filename, class_label, probability))
                db.commit()

            predictions.append({'filename': file.filename, 'class': class_label, 'probability': float(probability)})

        return jsonify(predictions)
    return render_template('index.html')

# Define a route for fetching prediction results
@app.route('/results', methods=['GET'])
def results():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            SELECT filename, class, probability FROM images
        ''')
        results = cursor.fetchall()
        return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')