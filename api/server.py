
# FASTAPI requirements
from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader, QuestionAnswerPrompt, GPTListIndex
from llama_index.indices.composability import ComposableGraph

from pydantic import BaseModel
from typing import Annotated
from llama_index import download_loader, ServiceContext
from PyPDF2 import PdfMerger




# Other requirements
import shutil
import pathlib
import os



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
                  files: list[UploadFile], 
                  embed_model = Annotated[str,Form()],
                  llm_model = Annotated[str,Form()]):
    

    merger = PdfMerger()

    for file in files :
        with open(f"current_active/_merge{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)


    for item in os.listdir('./current_active/'):
        if item.startswith('_merge'):
            #print(item)
            merger.append('./current_active/' + item)

    merger.write('./current_active/' + 'merged.pdf')
    merger.close()
    global current_filename, current_filetype, current_service_context, current_index, current_vector_index
    current_service_context = embeddings.get_service_context(embed_model, llm_model)
    current_filename = "merged.pdf"
    current_filetype = filetype


    

    #create embeddings
    current_vector_index,current_index = embeddings.create_embeddings(current_filename, current_filetype, current_service_context)


    return {"Embeddings created for file ":"done"}








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
    # index_list = []
    # summary_list=[]
    # PDFReader = download_loader("PDFReader")
    # current_service_context = embeddings.get_service_context(embed_model, llm_model)
    # for file in files:
    #         with open(f"current_active/{file.filename}", "wb") as buffer:
    #             shutil.copyfileobj(file.file, buffer)
    #         loader = PDFReader()
    #         doc = loader.load_data(f"current_active/{file.filename}")

    #         index = GPTListIndex.from_documents(doc,service_context=current_service_context)
    #         index_list.append(index)
    #         summary_list.append(str(index.query("What is a summary of this document?", response_mode="tree_summarize")))

    merger = PdfFileMerger()

    for file in files :
        with open(f"current_active/_merge{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)


    for item in os.listdir('./current_active/'):
        if item.startswith('_merge'):
            #print(item)
            merger.append('./current_active/' + item)

    merger.write('./current_active/' + 'merged.pdf')
    merger.close()

    global current_filename, current_filetype, current_service_context, current_index, current_vector_index
    current_service_context = embeddings.get_service_context(embed_model, llm_model)
    current_filename = "merged.pdf"
    current_filetype = "pdf"
    

    # graph = ComposableGraph.from_indices(
    #     GPTListIndex,
    #     index_list,
    #     index_summaries=summary_list,service_context=current_service_context)
    
    #graph.save_to_disk("data/graph.json")
# embeddings.create_embeddings(current_filename, current_filetype, current_service_context)[1]
# current_vector_index,current_index = embeddings.create_embeddings(current_filename, current_filetype, current_service_context)
    return "Embeddings created for all the files"

@app.post("/multi_query")
async def multi_query(query : Annotated[str,Form()]) :
    

    service_context = ServiceContext.from_defaults(chunk_size_limit=256)

    graph = ComposableGraph.load_from_disk("data/graph.json",service_context=current_service_context)

    return graph.query("You are a large language model whose expertise is finding most precise answers to the query requested. You are given a query and a series of summaries from the research paper. Your task is take these summaries and generate an accurate and precise response to the user's query.   User's Query is : "+query+"  Answer : ")
