import ocrmypdf

def get_ocr_done(file):
    ocrmypdf.ocr(f"./current_active/{file}", f"./current_active/{file}", deskew=True)