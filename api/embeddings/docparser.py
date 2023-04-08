from pathlib import Path
from llama_index import download_loader

from llama_index import SimpleDirectoryReader
PDFReader = download_loader("PDFReader")

def getdocument(filename : str,filetype:str):
    if filetype == "pdf":
        loader = PDFReader()
    elif filetype == "txt":
        loader = SimpleDirectoryReader('./example')



    
    document = loader.load_data(file=Path(filename))
    return document