
# FASTAPI requirements
from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from typing import Annotated




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
current_index = None
current_service_context = None





#initial processing of document
@app.post("/process")
async def process(filetype : Annotated[str,Form()], 
                  file: UploadFile = File(...), 
                  embed_model = Annotated[str,Form()],
                  llm_model = Annotated[str,Form()]):
    

    global current_filename, current_filetype, current_service_context, current_index
    current_service_context = embeddings.get_service_context(embed_model, llm_model)
    current_filename = file.filename
    current_filetype = filetype


    # save the file locally
    with open(f"current_active/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    

    #create embeddings
    current_index = embeddings.create_embeddings(current_filename, current_filetype, current_service_context)


    return {"Embeddings created for file":file.filename}








#ask questions on processed document
@app.post("/query")
async def query(query : Annotated[str, Form()]):
    
    print(current_filename)
    res = embeddings.query(query,current_filename,current_service_context)
    
    print(res)

    return res

# summarize processed document
@app.post("/summarize")
async def summarize():

    if current_index is None :
        return {"Error":"No file currently processed"}
    
    res = embeddings.summarize_doc(current_index)

    return res

@app.post("/summarizequery")
async def summarizequery(query : Annotated[str, Form()]):

    if current_index is None :
        return {"Error":"No file currently processed"}
    
    res = embeddings.summarizequery_query(query,current_index)

    return res