from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Import functions from your existing script
from legal_headless import main as analyze_legal_document

app = Flask(__name__)
# Enable CORS for your Next.js frontend
CORS(app)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Hello, World!'}), 200

@app.route('/analyze', methods=['POST'])
def analyze_document():
    try:
        # Check if a file was uploaded
        if 'file' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No file provided'
            }), 400
            
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'No file selected'
            }), 400
            
        if file and allowed_file(file.filename):
            # Secure the filename and save the file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Run the analysis with the uploaded file
            result = analyze_legal_document(filepath)
            
            # Clean up - remove the uploaded file after analysis
            os.remove(filepath)
            
            return jsonify({
                'status': 'success',
                'result': result
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Invalid file type. Only PDF files are allowed.'
            }), 400
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 42069))
    app.run(host='0.0.0.0', port=port, debug=True)