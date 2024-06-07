# Fashion Item Classifier

The Fashion Item Classifier is a machine learning application that automatically classifies fashion items into categories based on input images. It is designed to assist in the sorting process of refund items for an online shopping platform, reducing the manual effort required.

## Features

- Batch processing of multiple images for classification
- RESTful API for easy integration with other systems
- Containerization using Docker for easy deployment and scalability
- Automated deployment to a VPS using GitHub Actions
- SQLite database for storing classification results
- User-friendly web interface for uploading images and viewing results

## Project Structure

The project has the following structure:

```
├── .github
│   └── workflows
│       └── main.yml
├── app
│   └── static
│       └── uploads
├── data
│   └── styles.csv
│   └── images
│── templates
│   └── index.html
├── model
│   └── model.keras
├── test-images
├── app.py
├── batch_processing.py
├── db_setup.py
├── Dockerfile
└── requirements.txt
```

- `.github/workflows/main.yml`: GitHub Actions workflow for automated deployment to the VPS.
- `app/static/uploads`: Directory for storing uploaded images.
- `data/styles.csv`: Dataset containing fashion item categories and corresponding image URLs.
- `data/images`: Directory for storing images downloaded from the dataset.
- `templates/index.html`: HTML template for the web interface.
- `model/model.keras`: Trained Keras model file for fashion item classification.
- `test-images`: Directory containing sample images for testing.
- `app.py`: Flask application code for the API and web interface.
- `batch_processing.py`: Script for testing batch processing functionality.
- `db_setup.py`: Script for setting up the SQLite database.
- `Dockerfile`: Dockerfile for building the application container.
- `requirements.txt`: List of Python dependencies required for the project.

## Installation and Setup

1. Clone the repository:
   ```
   git clone https://github.com/mohamadsolouki/Batch-Processing.git
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up the SQLite database:
   ```
   python db_setup.py
   ```

4. Build the Docker image:
   ```
   docker build -t fashion-item-classifier .
   ```

5. Run the Docker container:
   ```
   docker run -d -p 5000:5000 --name fashion-item-classifier fashion-item-classifier
   ```

6. Access the web interface by opening a web browser and navigating to `http://localhost:5000`.

## Usage

### Web Interface

1. Open the web interface by accessing `http://localhost:5000` in a web browser.
2. Click on the "Choose Files" button to select one or more images for classification.
3. Click the "Upload Image(s)" button to upload the selected images.
4. The classification results will be displayed below, showing the top 3 predicted classes for each image.
5. Click the "Click to show previous predictions" button to view the classification results stored in the database.

### API

You can also use the RESTful API to classify images programmatically. Here's an example using Python:

```python
import requests

url = 'http://localhost:5000/predict'
files = [
    ('files[]', ('image1.jpg', open('path/to/image1.jpg', 'rb'), 'image/jpeg')),
    ('files[]', ('image2.jpg', open('path/to/image2.jpg', 'rb'), 'image/jpeg')),
    # Add more files as needed
]

response = requests.post(url, files=files)
predictions = response.json()

print(predictions)
```

Make sure to replace `'http://localhost:5000/predict'` with the actual URL where your application is hosted.

### Batch Processing

To test the batch processing functionality, you can run the `batch_processing.py` script:

```
python batch_processing.py
```

This script sends a batch of images in test-images directory to the API for classification and prints the results.

## Deployment

The project is set up for automated deployment to a VPS using GitHub Actions. Whenever a push is made to the `main` branch, the workflow defined in `.github/workflows/main.yml` is triggered. It builds the Docker image, pushes it to Docker Hub, and then deploys it to the specified VPS using SSH.

To configure the deployment:

1. Set up the necessary secrets in your GitHub repository settings:
   - `DOCKER_USERNAME`: Your Docker Hub username.
   - `DOCKER_PASSWORD`: Your Docker Hub password.
   - `VPS_HOST`: The hostname or IP address of your VPS.
   - `VPS_USERNAME`: The username for SSH access to your VPS.
   - `VPS_PASSWORD`: The password for SSH access to your VPS.

2. Push your changes to the `main` branch, and the deployment workflow will be triggered automatically.

## Contributing

Contributions to the Fashion Item Classifier project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).
