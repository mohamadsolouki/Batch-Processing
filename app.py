import os
import tensorflow as tf
from flask import Flask, request, render_template, jsonify, g
from tensorflow.keras.preprocessing import image # type: ignore
import numpy as np
import sqlite3

# Create app/static/uploads folder if it doesn't exist
if not os.path.exists('app/static/uploads'):
    os.makedirs('app/static/uploads')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
app.config['DATABASE'] = 'app/database.db'  # Define the database path

# Load the trained model
model = tf.keras.models.load_model('model/model.keras')

# Define the class labels (make sure these match your training data)
class_names = ['Bags', 'Belts', 'Bottomwear', 'Eyewear', 'Flip Flops', 'Fragrance', 'Innerwear',
              'Jewellery', 'Sandal', 'Shoes', 'Topwear', 'Wallets', 'Watches']

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
            predictions TEXT
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    db.commit()

# Define a function to preprocess the image
def preprocess_image(img):
    img = img.resize((160, 120))  # Resize to match your model input
    img = image.img_to_array(img)
    img = img / 255.0  # Rescale pixel values
    img = np.expand_dims(img, axis=0) 
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
            img = image.load_img(file_path, target_size=(160, 120))  # Match model input
            img = preprocess_image(img)

            # Make the prediction
            prediction = model.predict(img)
            top_indices = prediction[0].argsort()[-3:][::-1]
            top_predictions = [(class_names[idx], float(prediction[0][idx])) for idx in top_indices]

            # Save the prediction to the database
            with app.app_context():
                db = get_db()
                cursor = db.cursor()
                cursor.execute('''
                    INSERT INTO images (filename, predictions, timestamp)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                ''', (file.filename, ', '.join([f"{c}: {p:.2f}" for c, p in top_predictions])))
                db.commit()

            predictions.append({'filename': file.filename, 'predictions': top_predictions})

        return jsonify(predictions)
    return render_template('index.html')

# Define a route for fetching prediction results
@app.route('/results', methods=['GET'])
def results():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            SELECT filename, predictions, timestamp FROM images
        ''')
        results = [dict(row) for row in cursor.fetchall()]
        return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')