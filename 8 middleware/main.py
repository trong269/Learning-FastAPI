from urllib.request import Request
from fastapi import FastAPI, File, UploadFile
from typing import Annotated
import time
app = FastAPI()

@app.get('/')
async def root():
    return 'Hello World!'

@app.post("/files/")
async def creat_file(file :Annotated[ bytes, File()]):
    return {'file size: ' : len(file)}

@app.post("/uploadfile/")
async def create_file( file : UploadFile ):
    return {'file name: ' : file.filename}

# Định nghĩa một middleware
'''
    middleware used for process request and response
'''
@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response