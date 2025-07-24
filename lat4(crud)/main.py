from fastapi import FastAPI
from routes import mahasiswa, dosen
import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(mahasiswa.router, prefix="/mahasiswa", tags=["Mahasiswa"])
app.include_router(dosen.router, prefix="/dosen", tags=["Dosen"])
