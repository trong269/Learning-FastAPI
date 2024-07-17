from fastapi import FastAPI, File, UploadFile
from typing import Annotated

app = FastAPI()
'''
using File : chỉ đọc được nội dung , phù hợp với file nhỏ 
using UploadFile : đọc được toàn bộ data, có thể uplođ được file lớn và nhiều file
'''
@app.get('/')
async def root():
    return {"message": "Hello world"}
@app.post("/files/")
async def creat_file(file :Annotated[ bytes, File()]):
    return {'file size: ' : len(file)}

@app.post("/uploadfile/")
async def create_file( file : UploadFile ):
    return {'file name: ' : file.filename}