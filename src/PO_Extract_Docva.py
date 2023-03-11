def PO_Fields_Extract(p, doc):
    questions = {"PO_Number": ["What is the P.O. Number?", "what is P.O. No", "what is PO #", "what is purchase order #"],
                 "Shipping_Method": ["What is the shipping method?"],
                 "Shipping_Terms": ["what is the shipping terms?"],
                 "Date": ["What is date?"],
                 "Tax_Rate": ["what is tax rate?"],
                 "Tax_Amount": ["what is tax amount?"],
                 "Shipping_Amount": ["what is shipping amount?"],
                 "Total_Amount": ["what is total amount?"]}


    keys = ['PO_Number', 'Shipping_Method', 'Shipping_Terms', 'Date', 'Tax_Rate', 'Tax_Amount',
                               'Shipping_Amount', 'Total_Amount']
    extracted_fields = dict.fromkeys(keys, None)
    for i, q in enumerate(questions):
        print(q)
        for j, q1 in enumerate(questions[q]):
            score = 0
            answer = ''
            output = p(question=q1, **doc.context)
            print(output)
            if j == 0:
                score = output['score']
                answer = output['answer']
            elif score < output['score']:
                score = output['score']
                answer = output['answer']
        # print('\n')
        if (keys[i] == 'Date') and (score >0.3):
            extracted_fields[keys[i]] = {'value': output['answer'], 'probability': round(100*int(output['score']), 2)}
        elif (keys[i] == 'Tax_Rate') and (answer[-1] == '%') & (score > 0.5):
            extracted_fields[keys[i]] = {'value': output['answer'], 'probability': round(100*int(output['score']), 2)}
        elif (keys[i] == 'Tax_Amount') and (answer[-1] != '%') & (score > 0.5):
            extracted_fields[keys[i]] = {'value': output['answer'], 'probability': round(100*int(output['score']), 2)}
        elif (keys[i] not in ['Date', 'Tax_Rate', 'Tax_Amount']) and (score > 0.5):
            extracted_fields[keys[i]] = {'value': output['answer'], 'probability': round(100*int(output['score']), 2)}
    return extracted_fields


