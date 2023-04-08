from embeddings import get_service_context



def summarize_doc(index, service_context=None):

    response = index.query(
        "Provide a summary of the entire paper",  
        service_context=service_context,
        verbose=True,
        response_mode="tree_summarize"
    )
    return response

def summarize_query(index):
    pass

