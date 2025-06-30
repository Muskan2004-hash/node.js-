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
        # Save file temporarily to get size
        filepath = os.path.join("/tmp", filename)
        file.save(filepath)
        size = os.path.getsize(filepath)

        # Upload to S3
        with open(filepath, "rb") as f:
            s3.upload_fileobj(f, BUCKET, filename)

        # File info
        file_ext = os.path.splitext(filename)[1]
        file_data = {
            "filename": filename,
            "extension": file_ext,
            "size": f"{size} bytes"
        }

        # Save to MongoDB
        inserted = collection.insert_one(file_data)
        os.remove(filepath)

        # Add _id in response
        file_data["_id"] = str(inserted.inserted_id)

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
        result['_id'] = str(result['_id'])  # Convert ObjectId to string
        return jsonify(result), 200
    else:
        return jsonify({'error': 'File not found in MongoDB'}), 404

# === Run App ===
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
