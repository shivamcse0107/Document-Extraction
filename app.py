from flask import Flask, request, make_response, jsonify
import os
import warnings 
from src.main import Data_Extraction
from src.PDF_to_Image_Conversion import Covert_From_Location
from read_params import read_params

config = read_params('config.yaml')
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'png'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
warnings.filterwarnings('ignore')

app = Flask(__name__)

@app.errorhandler(400)
def handle_400_error(_error):
    return make_response(jsonify({'error': 'Misunderstood'}), 400)

@app.errorhandler(401)
def handle_401_error(_error):
    return make_response(jsonify({'Error': 'Unauthorised'}), 401)

@app.errorhandler(404)
def handle_404_error(_error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(500)
def handle_500_error(_error):
    return make_response(jsonify({'error': 'Server error'}), 500)

@app.route("/files_v1.0", methods=['POST', 'GET'])
def files():
    if request.method =='POST':
        file_path = request.files["file_path"]
        document_type = request.args.get('Document_type')
        document_type = ""
        if os.path.isfile(config['base']['convert_path']):
            os.remove(config['base']['convert_path'])
        if file_path:
            if allowed_file(file_path.filename):

                file_location = os.path.join(
                    config['base']['UPLOAD_FOLDER'],
                    file_path.filename
                    )
                file_path.save(file_location)
            else:
                return make_response(jsonify({'error': 'Please Upload file in png ,jpg or pdf.','status': 404}))
        else:
            return make_response(jsonify({'error': 'File does not exist please upload','status': 404}))
        
        if file_path.filename.endswith(".pdf"):
            try:
                Covert_From_Location(path=file_location)
            except Exception:
                return make_response(jsonify({'error': 'Model is not able to change pdf into png or jpg.','status': 404}))
            
            try:
                prediction = Data_Extraction(config['base']['convert_path'], form_type=document_type)
                return jsonify({'extraction_result': prediction,'status': 200})
            except Exception:
                return make_response(jsonify({'error': 'Model is not able to predict please try again.','status': 404}))
        else:
            try:
                prediction = Data_Extraction(path=file_location, form_type=document_type)
                return make_response(jsonify({'extraction_result': prediction,'status': 200}))
            except Exception:
                return make_response(jsonify({'error': 'Model is not able to predict please try again.','status': 404}))

if __name__ =="__main__":
    app.run(host = "0.0.0.0",port=3009, debug=True)
