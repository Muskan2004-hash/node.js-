
from flask import Flask, request, jsonify
import os
import boto3

app = Flask(__name__)

s3 = boto3.client('s3')
BUCKET = os.environ.get('S3_BUCKET', 'file-info-bucket')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    s3.upload_fileobj(file, BUCKET, filename)
    return jsonify({'message': 'Uploaded to S3', 'filename': filename})

@app.route('/fileinfo', methods=['POST'])
def file_info():
    data = request.get_json()
    filename = data.get('filename')

    if not filename:
        return jsonify({'error': 'No filename provided'}), 400

    file_extension = os.path.splitext(filename)[1]
    fake_size = len(filename) * 123

    return jsonify({
        'filename': filename,
        'extension': file_extension,
        'size': f'{fake_size} bytes'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
