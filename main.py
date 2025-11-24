import uvicorn 
from fastapi import FastAPI
from src import webhook

app = FastAPI()

app.include_router(webhook.router, prefix='', tags=['/'])

if __name__ == "__main__":
    # uvicorn.run("webhook:app", host="0.0.0.0", port=8000, reload=True)
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)