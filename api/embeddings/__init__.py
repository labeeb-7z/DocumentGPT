res = 0

from .create_embeddings import create_embeddings
from .service_context import get_service_context
from .query import query_qna, query_highlight

from .summarize import summarize_doc
from .ocr import get_ocr_done