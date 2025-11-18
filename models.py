from sqlalchemy import Column, Integer, String
from database import Base

class Imagem(Base):
    __tablename__ = "imagens"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    tag = Column(String, nullable=False)

