from flask import Flask, request, jsonify
from utils import preprocess_images, predict_batch

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    images = request.files.getlist('images')
    preprocessed_images = preprocess_images(images)
    predictions = predict_batch(preprocessed_images)
    return jsonify({'predictions': predictions.tolist()})

if __name__ == '__main__':
    app.run()