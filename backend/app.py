from flask import Flask, request, jsonify
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import os
import boto3
from bson import ObjectId

app = Flask(__name__)

# === S3 Setup ===
s3 = boto3.client('s3')
BUCKET = os.environ.get('S3_BUCKET', 'file-info-bucket')

# === MongoDB Setup ===
mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
mongo_client = MongoClient(mongo_uri)
db = mongo_client["fileinfo_db"]
collection = db["files"]

# === Upload Endpoint ===
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filename = secure_filename(file.filename)

    try:
        # Save file temporarily to calculate size
        temp_path = os.path.join("/tmp", filename)
        file.save(temp_path)
        size = os.path.getsize(temp_path)

        # Upload to S3
        with open(temp_path, "rb") as f:
            s3.upload_fileobj(f, BUCKET, filename)

        # File info
        file_ext = os.path.splitext(filename)[1]
        file_data = {
            "filename": filename,
            "extension": file_ext,
            "size": f"{size} bytes"
        }

        # Save metadata to MongoDB
        collection.insert_one(file_data)

        # Clean up temp file
        os.remove(temp_path)

        return jsonify({
            'message': 'Uploaded to S3 and saved to MongoDB',
