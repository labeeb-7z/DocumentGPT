from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from llama_index import LangchainEmbedding, ServiceContext, LLMPredictor
from langchain import OpenAI, HuggingFaceHub
from langchain.chat_models import ChatOpenAI

import embeddings.prompt_helper as prompt_helper


def get_service_context(embed="HF", llm="OpenAI"):


    embed_model = LangchainEmbedding(HuggingFaceEmbeddings())

    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003", max_tokens=256))
    #llm_predictor = LLMPredictor(llm=HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.9}))
    
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, embed_model=embed_model, prompt_helper=prompt_helper.prompt_helper, chunk_size_limit=256)


    return service_context
