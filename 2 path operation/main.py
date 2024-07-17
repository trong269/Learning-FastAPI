from fastapi import FastAPI
'''
get : receive 
post : receive 
put : update
delete : delete
'''
app = FastAPI()

@app.get('/')
async def root():
    return 'Hello World'