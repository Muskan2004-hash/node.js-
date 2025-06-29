from flask import Flask, request, jsonify
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import os
import boto3

app = Flask(__name__)

# === S3 Setup ===
s3 = boto3.client('s3')
BUCKET = os.environ.get('S3_BUCKET', 'file-info-bucket')

# === MongoDB Setup ===
# Use environment variable or default to localhost
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
        # Upload to S3
        s3.upload_fileobj(file, BUCKET, filename)

        # Get actual size
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file_ext = os.path.splitext(filename)[1]

        # Save to MongoDB
        file_data = {
            "filename": filename,
            "extension": file_ext,
            "size": f"{size} bytes"
        }
        collection.insert_one(file_data)

        return jsonify({
            'message': 'Uploaded to S3 and saved to MongoDB',
            **file_data
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# === Retrieve File Info ===
@app.route('/fileinfo', methods=['POST'])
def file_info():
    data = request.get_json()
    filename = data.get('filename')

    if not filename:
        return jsonify({'error': 'No filename provided'}), 400

    result = collection.find_one({"filename": filename})
    if result:
        return jsonify({
            'filename': result['filename'],
            'extension': result['extension'],
            'size': result['size']
        })
    else:
        return jsonify({'error': 'File not found in MongoDB'}), 404

# === Run App ===
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
