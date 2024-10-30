from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Import functions from your existing script
from legal_headless import main as analyze_legal_document

app = Flask(__name__)
# Enable CORS for your Next.js frontend
CORS(app)

# Load environment variables
load_dotenv()

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Hello, World!'}), 200

@app.route('/analyze', methods=['GET'])
def analyze_document():
    try:
        # Run the analysis
        result = analyze_legal_document()
        
        return jsonify({
            'status': 'success',
            'result': result
        }), 200
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 42069))
    app.run(host='0.0.0.0', port=port, debug=True)