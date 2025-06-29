from flask import Flask, request, jsonify
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import os
import boto3

app = Flask(__name__)

# S3 Setup
s3 = boto3.client('s3')
BUCKET = os.environ.get('S3_BUCKET', 'file-info-bucket')

# MongoDB Setup
mongo_client = MongoClient("mongodb://13.235.116.123:27017/")
db = mongo_client["fileinfo_db"]
collection = db["files"]

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = secure_filename(file.filename)

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
    })

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


