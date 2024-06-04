# Fashion Item Image Classifier

This application classifies images of fashion items into categories like Apparel, Accessories, Footwear, etc., using a trained deep learning model. It's built with Flask, TensorFlow, and Docker for easy deployment.

## Features

- **Image Upload:** Upload one or more fashion item images.
- **Real-time Predictions:** Get instant predictions on the uploaded images.
- **Dockerized Deployment:** Easily deploy the application using Docker.
- **GitHub Actions CI/CD:** Automated build and deployment workflow with GitHub Actions.

## Project Structure

├── app
│   ├── static
│   │   └── uploads
│   └── templates
│       └── index.html
├── model
│   └── fashion_model.h5
├── app.py
├── Dockerfile
├── requirements.txt
├── .github
│   └── workflows
│       └── main.yml
└── README.md


## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Build the Docker Image:**
   ```bash
   docker build -t your-dockerhub-username/fashion-classifier .
   ```

## Usage

1. **Run the Docker Container:**
   ```bash
   docker run -d -p 5000:5000 --name fashion-classifier your-dockerhub-username/fashion-classifier
   ```

2. **Access the Application:**
   Open your web browser and go to `http://localhost:5000/` (or your server's IP address if deployed remotely).

3. **Upload Images:**
   Click on the "Choose Files" button to select one or more images from your computer.

4. **View Predictions:**
   The predicted class and probability for each image will be displayed below the upload button.

## Deployment

This project is set up for automated deployment using GitHub Actions. Every push to the `main` branch will trigger the workflow:

- Build the Docker image.
- Push the image to Docker Hub.
- SSH into your VPS (using credentials stored as GitHub Secrets).
- Update the running Docker container on your VPS.

## Technologies Used

- **Flask:** Python web framework.
- **TensorFlow/Keras:** Machine learning library for building and loading the model.
- **Docker:** Containerization platform for easy deployment.
- **GitHub Actions:** CI/CD platform for automated build and deployment.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
