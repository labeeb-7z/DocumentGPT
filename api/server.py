
# FASTAPI requirements
from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader, QuestionAnswerPrompt, GPTListIndex
from llama_index.indices.composability import ComposableGraph

from pydantic import BaseModel
from typing import Annotated, List
from llama_index import download_loader, ServiceContext
from PyPDF2 import PdfMerger




# Other requirements
import shutil
import pathlib
import os
from pathlib import Path
import markdown2
import pdfkit
import glob

# Custom modules
import embeddings
#####



#init APP
app = FastAPI()
origins = [
    "*"
]
#handle cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#idk what this does
class PDFModel(BaseModel):
    file: UploadFile = File(...)



#what are you doing on this route?
@app.get("/")
async def root():
    return {"???????????"}

@app.get("/")
async def root() :
    return {"helo world"}




current_filename = None
current_filetype = None
current_vector_index = None
current_index = None
current_service_context = None
similarity=None





#initial processing of document
@app.post("/process")
async def process(filetype : Annotated[str,Form()], 
                  files: List[UploadFile],
                  embed_model : Annotated[str,Form()],
                  llm_model : Annotated[str,Form()],
                  ocr : Annotated[str,Form()]) :
    
    redundant = glob.glob('./current_active/*')
    for r in redundant :
        os.remove(r)
    
    redundant = glob.glob('./data/*')
    for r in redundant :
        os.remove(r)

    merger = PdfMerger()

    for file in files :
        with open(f"current_active/_merge{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    for item in os.listdir('./current_active/'):
        if item.startswith('_merge'):
            if ocr == "true" :
                print("inside ocr")
                embeddings.get_ocr_done(item)
            merger.append('./current_active/' + item)
            os.remove('./current_active/' + item)

    merger.write('./current_active/' + 'merged.pdf')
    merger.close()
    global current_filename, current_filetype, current_service_context, current_index, current_vector_index,similarity
    if llm_model=="HF" : 
        similarity=1
    current_service_context = embeddings.get_service_context(embed_model, llm_model)
    current_filename = "merged.pdf"
    current_filetype = filetype


    

    #create embeddings
    current_vector_index,current_index = embeddings.create_embeddings(current_filename, current_filetype, current_service_context)


    #return {"Embeddings created for file ":"done"}
    return {"response":"Embeddings created for given file"}








#ask questions on processed document
@app.post("/queryqna")
async def query(query : Annotated[str, Form()]):
    
    res = embeddings.query_qna(query,current_filename,current_service_context,similarity)

    print(res)

    return res

@app.post("/queryhighlight")
async def query(query : Annotated[str, Form()], context : Annotated[str, Form()]):
    
    print("queryhighlight called")
    res = embeddings.query_highlight(query,current_filename,current_service_context,similarity)
    

    return res





# summarize processed document
@app.post("/summarize")
async def summarize():

    if current_index is None :
        return {"Error":"No file currently processed"}
    
    res = embeddings.summarize_doc(current_index,current_service_context)

    return res

@app.post("/summarizequery")
async def summarizequery(query : Annotated[str, Form()]):

    if current_index is None :
        return {"Error":"No file currently processed"}
    
    res = embeddings.summarizequery_query(query,current_index)

    return res

# To get a topic from user and load papers
@app.post("/arxiv")
async def arxiv(topic:  Annotated[str, Form()]):
    ArxivReader = download_loader("ArxivReader")
    loader = ArxivReader()
    document = loader.load_data(search_query=topic, max_results=5) 

    index = GPTSimpleVectorIndex.from_documents(document,service_context=current_service_context)
    index.save_to_disk(f"./data/arxiv.json") # Will create a file
    return {"response" : "Papers loaded"}

@app.post("/arxiv_query")
async def arxiv_query(question : Annotated[str, Form()]):
    index = GPTSimpleVectorIndex.load_from_disk(f"./data/arxiv.json", service_context=current_service_context)
    res=index.query(question, similarity_top_k=3,verbose=True,response_mode="compact")

    return res

# submit a url and convert to the index
@app.post("/url")
async def url(link:Annotated[str, Form()]):
    if link.find('youtube') != -1:
        YoutubeTranscriptReader = download_loader("YoutubeTranscriptReader")
        loader = YoutubeTranscriptReader()
        document = loader.load_data([link])
        index = GPTSimpleVectorIndex.from_documents(document,service_context=current_service_context)
        # index = GPTListIndex.from_documents(document,service_context=current_service_context)

    else:
        SimpleWebPageReader = download_loader("SimpleWebPageReader")
        loader = SimpleWebPageReader()
        document = loader.load_data([link])
        index = GPTSimpleVectorIndex.from_documents(document,service_context=current_service_context)
        # index = GPTListIndex.from_documents(document,service_context=current_service_context)
    index.save_to_disk(f"./data/url.json")

    return {"response" : "URL loaded"}

# ask a question from the submited url
@app.post("/url_query")
async def url_query(question: Annotated[str, Form()]):
    index = GPTSimpleVectorIndex.load_from_disk(f"./data/url.json", service_context=current_service_context)
    res=index.query(question, similarity_top_k=3, verbose=True,response_mode="compact")
    return res

@app.post("/md")
async def md(md_file: UploadFile = File(...)):
    # with open(md_file, 'r') as file:
    #     markdown_contents = file.read()
    with open(f"current_active/{md_file.filename}", "wb") as buffer:
        shutil.copyfileobj(md_file.file, buffer)
    with open(f"current_active/{md_file.filename}", 'r') as file:
        markdown_contents = file.read()
    html_contents = markdown2.markdown(markdown_contents)
    file=pdfkit.from_string(html_contents, f"./current_active/md_pdf.pdf")
    filetype='pdf'
    embed_model="HF"
    llm_model="OpenAI"
    global current_filename, current_filetype, current_service_context
    current_service_context = embeddings.get_service_context(embed_model, llm_model)
    current_filename = "md_pdf.pdf"
    current_filetype = "pdf"

    index = embeddings.create_embeddings(current_filename, current_filetype, current_service_context)

    return {"Markdown upload":"Success"}


@app.post("/md_query")
async def md_query(query : Annotated[str, Form()]):
    
    print(current_filename)
    res = embeddings.query_qna(query,current_filename,current_service_context)
    
    return res

