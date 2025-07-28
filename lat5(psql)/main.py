from fastapi import FastAPI
from routes.route import itemrouter

app = FastAPI()
app.include_router(itemrouter)