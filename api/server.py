
# FASTAPI requirements
from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader, QuestionAnswerPrompt, GPTListIndex

from pydantic import BaseModel
from typing import Annotated
from llama_index import download_loader




# Other requirements
import shutil




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
@app.post("/")
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






#initial processing of document
@app.post("/process")
async def process(filetype : Annotated[str,Form()], 
                  file: UploadFile = File(...), 
                  embed_model = Annotated[str,Form()],
                  llm_model = Annotated[str,Form()]):
    

    global current_filename, current_filetype, current_service_context, current_index, current_vector_index
    current_service_context = embeddings.get_service_context(embed_model, llm_model)
    current_filename = file.filename
    current_filetype = filetype


    # save the file locally
    with open(f"current_active/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    

    #create embeddings
    current_vector_index,current_index = embeddings.create_embeddings(current_filename, current_filetype, current_service_context)


    return {"Embeddings created for file ":file.filename}








#ask questions on processed document
@app.post("/queryqna")
async def query(query : Annotated[str, Form()]):
    
    res = embeddings.query_qna(query,current_filename,current_service_context)


    return res

@app.post("/queryhighlight")
async def query(query : Annotated[str, Form()], context : Annotated[str, Form()]):
    
    print("queryhighlight called")
    res = embeddings.query_highlight(query,current_filename,current_service_context)
    

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
    document = loader.load_data(search_query=topic, max_results=1) # How to get max 3 results?

    index = GPTSimpleVectorIndex.from_documents(document,service_context=current_service_context)
    index.save_to_disk(f"./data/arxiv.json") # Will create a file
    return "Papers fetched"

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

    return "url fetched"

# ask a question from the submited url
@app.post("/url_query")
async def url_query(question: Annotated[str, Form()]):
    index = GPTSimpleVectorIndex.load_from_disk(f"./data/url.json", service_context=current_service_context)
    # index = GPTListIndex.load_from_disk(f"./data/url.json", service_context=current_service_context)
    res=index.query(question, similarity_top_k=3, verbose=True,response_mode="compact")
    return res



