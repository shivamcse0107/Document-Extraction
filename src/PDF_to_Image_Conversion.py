from pdf2image import convert_from_path
destination_path = "converted_files/"

def Covert_From_Location(path):
    pages = convert_from_path(path, use_cropbox=True,poppler_path=r'C:\Program Files\poppler-0.67.0\bin')

    for i,page in enumerate(pages):
        page.save(destination_path+"page_"+str(i)+'.jpg', 'JPEG')
        # print(file)

