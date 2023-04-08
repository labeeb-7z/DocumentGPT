from llama_index import PromptHelper

max_input_size = 4096
num_output = 2048

chunk_size_limit = 256
max_chunk_overlap = 20
prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
