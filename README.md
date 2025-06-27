
# File Info App

A full-stack application that allows users to upload files and view file metadata.

## Tech Stack

- Frontend: Node.js (Express, EJS)
- Backend: Python (Flask)
- Storage: AWS S3
- Deployment: Docker & Docker Compose

## How to Run

```bash
docker-compose up --build
```

## S3 Integration

Make sure to set the following environment variables:

- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_DEFAULT_REGION
- S3_BUCKET
