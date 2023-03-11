def GR_DN_Fields_Extract(p,doc):
    questions = ["What is  invoice date?",
                 "what is  the location?",
                 "What is the Delivery method?",
                 "What is the carrier?",
                 "What is the total wight?"]

    keys = ['Date', 'Location', 'Delivery Method', 'Carrier', 'Total Weight']
    extracted_fields = dict.fromkeys(keys, None)
    for i, q in enumerate(questions):
        output = p(question=q, **doc.context)
        if output['score'] > 0.3:
            extracted_fields[keys[i]] = {'value': output['answer'], 'probability': round(100*int(output['score']), 2)}

    return extracted_fields

