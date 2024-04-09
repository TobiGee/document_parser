# document_parser
Small proof of concept for document parsing.

## Installations

### Qdrant
- Install docker (follow instruction from https://www.docker.com)
- Run 
```bash docker pull qdrant/qdrant ```
### OpenAI
- Set OpenAI Env Variable 
```bash export OPENAI_API_KEY=YOURKEY```
### venv
- Install requirements to conda venv
## Running
- Run Qdrant by 
```bash docker run -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage:z qdrant/qdrant```
- Download llama models from https://huggingface.co/mys/ggml_llava-v1.5-7b/tree/main
- start llama server (in seperate terminal and keep open) 
```bash python -m llama_cpp.server --model llava/ggml-model-q5_k.gguf --clip_model_path llava/mmproj-model-f16.gguf --chat_format llava-1-5 --n_gpu_layers 1 --n_threads 8```
- Activate conda venv in new terminal instance
- Run main.py 

