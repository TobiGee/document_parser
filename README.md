# document_parser
Small proof of concept for document parsing.

## Installations

### Qdrant
- Install docker (follow instruction from https://www.docker.com)
- Run ```bash docker pull qdrant/qdrant ```


## Running
- Run Qdrant by ```bash docker run -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage:z qdrant/qdrant```
- Activate venv
- Run main.py 

