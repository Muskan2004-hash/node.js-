📁 File Info Web App

A full-stack web application where users can upload files, and the system stores them on AWS S3 while saving file metadata (name, size, extension) into MongoDB. The project is fully containerized using Docker, and CI/CD is handled via Jenkins with deployment on AWS EC2.


🚀 Features

    🌐 Upload files via a simple Node.js/EJS frontend

    ☁️ File stored securely in Amazon S3

    🗃️ File metadata saved in MongoDB

    ⚙️ Backend built with Python Flask

    🐳 Dockerized frontend, backend & database

    🔁 Jenkins Pipeline automates deployment to AWS EC2

    🔐 Environment variables used to manage secrets securely

### 🧱 Tech Stack

| Layer       | Technology            |
|-------------|------------------------|
| Frontend    | Node.js, EJS, HTML/CSS |
| Backend     | Python, Flask          |
| Database    | MongoDB                |
| File Storage| AWS S3                 |
| DevOps      | Docker, Jenkins        |
| Cloud       | AWS EC2, S3            |


📦 Folder Structure

fileinfoapp/
├── backend/
│ └── app.py # Flask backend for file upload and info
├── frontend/
│ └── views/
│ └── index.ejs # EJS file upload form
├── docker-compose.yml # Multi-container orchestration
├── Jenkinsfile # CI/CD pipeline script 


🧪 API Endpoints
Method	Endpoint	   Description
POST	 /upload	    Upload file to S3 + save to DB
POST	 /fileinfo      Retrieve file metadata from DB


✅ Jenkins Pipeline (Deployment)

   1. Automatically clones the repo

   2. Injects AWS credentials securely

   3. SSHs into EC2 instance

   4. Runs docker-compose to deploy the app

 
 
