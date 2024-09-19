from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import PyPDF2

app = Flask(__name__)
CORS(app)

# Configure upload folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Hello, World!"})

@app.route('/api/example', methods=['POST'])
def handle_pdf_upload():
    if 'files' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    files = request.files.getlist('files')
    
    if not files or files[0].filename == '':
        return jsonify({"error": "No files selected"}), 400
    
    file_info = []
    processed_files = []
    
    for file in files:
        if file and file.filename.lower().endswith('.pdf'):
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            processed_files.append(file_path)
            
            # Process PDF file
            with open(file_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                total_chars = sum(len(page.extract_text()) for page in pdf_reader.pages)
            
            file_info.append({
                "filename": filename,
                "char_count": total_chars,
                "page_count": len(pdf_reader.pages)
            })
        else:
            file_info.append({
                "filename": file.filename,
                "error": "Not a PDF file"
            })
    
    # Delete all processed files
    for file_path in processed_files:
        os.remove(file_path)
    
    return jsonify({"files": file_info})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)