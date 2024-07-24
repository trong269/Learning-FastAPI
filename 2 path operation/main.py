from fastapi import FastAPI
'''
get : retrieve 
post : create 
put : update
delete : delete
'''
app = FastAPI()

@app.get('/')
async def root():
    return 'Hello World'