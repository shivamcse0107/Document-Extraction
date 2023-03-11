from docquery import document, pipeline
# p = pipeline("document-question-answering", model='impira/layoutlm-invoices')
# doc = document.load_document("D:\Invoices_data_extraction\doc_query_approach\Sample Documents\Accounts Payable\PR document samples\purchase-requisition-sample-1-771x1024.png")
def PR_Extracted_Fields(p, doc):
    questions = ["What is the  Requisition Number?", "What is the shipping method?",
                 "what is the  terms?", "What is date?","what is delivery date?",
                 "what is tax rate?", "what is tax amount?",
                 "what is shipping amount?", "what is total amount?"]


    keys = ['PR_Number', 'Shipping_Method', 'Shipping_Terms', 'Date','Delivery_date', 'Tax_Rate', 'Tax_Amount',
                               'Shipping_Amount', 'Total_Amount']
    extracted_fields = dict.fromkeys(keys, None)
    for i, q in enumerate(questions):
        # print(q)
        output = p(question=q, **doc.context)
        # print(output)
        # print('\n')
        if output['score'] > 0.3:
            extracted_fields[keys[i]] = {'value': output['answer'], 'probability': round(100*int(output['score']), 2)}
    return extracted_fields

# print(extracted_fields)
