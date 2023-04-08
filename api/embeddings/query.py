from llama_index import GPTSimpleVectorIndex, QuestionAnswerPrompt


def query_qna(text,filename,current_service_context, verbose=False):

    QA_PROMPT_TMPL = (
    """You are a large language model whose expertise is reading and summarizing documents. 
        You are given a query and a series of text embeddings from a document in order of their cosine similarity to the query.
        You must take the given embeddings and return a very precise response of the document that answers the query. The response should be as short as possible.
            
            Given the question:  {query_str} 
            
            and the following embeddings as data: 
            
            {context_str}

            Return a compact and precise and most accurate answer without any unnecesary details based on the paper: """
    )
    QA_PROMPT = QuestionAnswerPrompt(QA_PROMPT_TMPL)

    index = GPTSimpleVectorIndex.load_from_disk(f"./data/{filename}_vector.json", service_context=current_service_context)
    res = index.query(
        text,  
        verbose=True,
        similarity_top_k=3,
        text_qa_template=QA_PROMPT,
    )
    return res



def query_highlight(text,filename,current_service_context, verbose=False):

    QA_PROMPT_TMPL = (
    """You are a large language model whose expertise is reading and summarizing scientific papers. 
        You are given a highlighted text and a series of text embeddings from a paper in order of their cosine similarity to the query.
        The user wants more explanation and clarification on the highlighted text.
        You must take the given embeddings and return a very detailed summary of the paper that answers the query.
            
            Given the Highlighted Text:  {query_str} 
            
            and the following embeddings as data: 
            
            {context_str}

            Return a detailed explanation based on the paper: """
    )
    QA_PROMPT = QuestionAnswerPrompt(QA_PROMPT_TMPL)

    index = GPTSimpleVectorIndex.load_from_disk(f"./data/{filename}_vector.json", service_context=current_service_context)
    
    res = index.query(
        text,  
        verbose=True,
        similarity_top_k=3,
        text_qa_template=QA_PROMPT,
        response_mode="compact"
    )
    return res