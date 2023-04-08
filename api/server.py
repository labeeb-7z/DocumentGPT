
# FASTAPI requirements
from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader, QuestionAnswerPrompt, GPTListIndex
from llama_index.indices.composability import ComposableGraph

from pydantic import BaseModel
from typing import Annotated
from llama_index import download_loader




# Other requirements
import shutil
import pathlib



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
    
    print(current_filename)
    res = embeddings.query_qna(query,current_filename,current_service_context)
    
    print(res)

    return res

@app.post("/queryhighlight")
async def query(query : Annotated[str, Form()]):
    
    print(current_filename)
    res = embeddings.query_highlight(query,current_filename,current_service_context)
    
    print(res)

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
    return {"Success" : "Papers loaded"}

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
    index = GPTListIndex.load_from_disk(f"./data/url.json", service_context=current_service_context)
    res=index.query(question, similarity_top_k=3, verbose=True,response_mode="compact")
    return res

@app.post("/multi")
async def multi(files: list[UploadFile], embed_model = Annotated[str,Form()],llm_model = Annotated[str,Form()]):
    index_list = []
    summary_list=[]
    PDFReader = download_loader("PDFReader")
    current_service_context = embeddings.get_service_context(embed_model, llm_model)
    for file in files:
            with open(f"current_active/{file.filename}", "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            loader = PDFReader()
            doc = loader.load_data(f"current_active/{file.filename}")

            index = GPTListIndex.from_documents(doc)
            index_list.append(index)
            summary_list.append(str(index.query("What is a summary of this document?", response_mode="tree_summarize")))

            
    graph = ComposableGraph.from_indices(
        GPTListIndex,
        index_list,
        index_summaries=summary_list,)
    
    graph.save_to_disk("data/graph.json")
# embeddings.create_embeddings(current_filename, current_filetype, current_service_context)[1]
# current_vector_index,current_index = embeddings.create_embeddings(current_filename, current_filetype, current_service_context)
    return "Embeddings created for all the files"

@app.post("/multi_query")
async def multi_query(query : Annotated[str,Form()]) :
    graph = ComposableGraph.load_from_disk("data/graph.json")

    return graph.query("You are a large language model whose expertise is finding most precise answers to the query requested. You are given a query and a series of text embeddings from a paper in order of their cosine similarity to the query. You must take the given embeddings and return the most correct answer from the paper that answers the query."+query)
