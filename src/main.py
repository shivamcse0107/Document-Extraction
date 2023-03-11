from docquery import document, pipeline
from src.Invoice_Extract_Docva import Invoice_Fields_Extract
from src.PO_Extract_Docva import PO_Fields_Extract
from src.PR_Extract_Docva import PR_Extracted_Fields
from src.GR_DN_Extract_Docva import GR_DN_Fields_Extract
import warnings
from flask import Flask, request, make_response, jsonify

from read_params import read_params
config = read_params('config.yaml')

warnings.filterwarnings("ignore")
c_p = pipeline("document-question-answering", model=config['base']['classification_model'])
p = pipeline("document-question-answering", model=config['base']['extraction_model'])



document_classes = ['invoice', 'purchase order', 'delivery note', 'purchase request']

def Data_Extraction(path, form_type):

    if form_type == '':

        doc = document.load_document(path)
        q = ["what is document class?", "what is document type?"]
        for i in q:
            ans = c_p(question=i, **doc.context)
            if (str(ans['answer']).lower() in document_classes) or (str(ans['answer'].split(' ')[0]).lower() in document_classes):
                break
        if (str(ans['answer'].split(' ')[0])== 'invoice') or (str(ans['answer']) in document_classes):
            if str(ans['answer'].split(' ')[0])== 'invoice':
                form_type = str(ans['answer'].split(' ')[0]).lower()
            else:
                form_type = str(ans['answer'])

            if form_type == 'invoice':
                extracted_fields = Invoice_Fields_Extract(p, doc)
            elif form_type == 'purchase order':
                extracted_fields = PO_Fields_Extract(p, doc)
            elif form_type == 'purchase request':
                extracted_fields = PR_Extracted_Fields(p, doc)
            elif form_type == 'delivery note':
                extracted_fields = GR_DN_Fields_Extract(p, doc)
            else:
                return make_response(jsonify({'error':'Document not supported','status': 404}))

        else:
            return make_response(jsonify({'error':'Document not supported','status': 404}))
    else:
        doc = document.load_document(path)
        if form_type == 'invoice':
            print('processing invoice')
            extracted_fields = Invoice_Fields_Extract(p, doc)
        elif form_type == 'purchase order':
            extracted_fields = PO_Fields_Extract(p, doc)
        elif form_type == 'purchase request':
            extracted_fields = PR_Extracted_Fields(p, doc)
        elif form_type == 'delivery note':
            extracted_fields = GR_DN_Fields_Extract(p, doc)
        else:
            return make_response(jsonify({'error':'Document not supported','status': 404}))
    return extracted_fields


