import os
from flask import(
    Flask,
    request,
    render_template,
    redirect,
    send_from_directory,
    jsonify
)
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
import shutil
import dotenv
import jsonify

import json
import openai
import glob
import sys

sys.path.append("./scripts")
from generators import llm_json_generator


# load environment variables
try:
    dotenv.load_dotenv()
except Exception as e:
    print(f"An error occured while loading environment variables: {e}")

# check if OpenAI API key is set
if os.getenv("OPENAI_API_KEY") is not None:
    api_key_set = True
else:
    api_key_set = False

# routes
app = Flask(__name__)

@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_file():

    # empty output_files directory
    shutil.rmtree('output_files')
    os.mkdir('output_files')

    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        file_path = os.path.join('output_files', filename)
        file.save(file_path)

        output_list = llm_json_generator()

        with open('./output_files/example.json', 'w') as file:
            file.write(json.dumps(output_list))

        return "200"

    return jsonify({'error': 'Invalid file type, only PDF files are allowed'}), 400


@app.route('/get_json', methods=['GET'])
@cross_origin()
def get_json():
    with open('./output_files/example.json', 'r') as file:
        return file.read()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
