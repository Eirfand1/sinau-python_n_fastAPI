from sqlalchemy import Column, Integer, String
from database import Base

class Mahasiswa(Base):
    __tablename__ = "mahasiswa"
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String)
    nim = Column(String, unique=True, index=True)

class Dosen(Base):
    __tablename__ = "dosen"
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String)
    nip = Column(String, unique=True, index=True)
