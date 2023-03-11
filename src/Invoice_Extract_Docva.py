def Invoice_Fields_Extract(p,doc):
    questions = ["What is the invoice number?","what is invoice date?",
                 "What is due date?","what is PO Number?",
                 "What is the balance due?", "what is total amount?"]

    keys = ['Invoice_Number', 'Invoice_date', 'Due_Date', 'PO_Number', 'Balance_Due', 'Total_Amount']
    extracted_fields = dict.fromkeys(keys, None)
    for i, q in enumerate(questions):
        output = p(question=q, **doc.context)
        if output['score'] > 0.5:
            extracted_fields[keys[i]] = {'value': output['answer'], 'probability': round(100*(output['score']), 2)}

    return extracted_fields

