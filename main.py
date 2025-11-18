from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import socket
import httpx
from typing import List
from pydantic import BaseModel
import logging

from database import engine, get_db, Base
from models import Imagem

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="API de Imagens")

@app.on_event("startup")
async def startup_event():
    """
    Tenta criar as tabelas no banco ao iniciar a aplicação.
    Se falhar, a API ainda será iniciada (útil para teste do endpoint de hostname).
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tabelas do banco de dados criadas/verificadas com sucesso!")
    except Exception as e:
        logger.error(f"⚠️  Erro ao conectar/criar tabelas no banco: {str(e)}")
        logger.warning("A API será iniciada, mas endpoints que dependem do banco podem falhar.")

class ImagemResponse(BaseModel):
    id: int
    url: str
    tag: str
    
    class Config:
        from_attributes = True

class TagResponse(BaseModel):
    tags: List[str]

class UploadResponse(BaseModel):
    message: str
    id: int
    url: str
    tag: str

class HostnameResponse(BaseModel):
    hostname: str

@app.get("/", response_model=HostnameResponse)
def get_hostname():
    """
    Retorna o hostname da máquina para verificar o balanceamento de carga.
    """
    hostname = socket.gethostname()
    return {"hostname": hostname}

@app.get("/health")
def health_check():
    """
    Verifica o status da API e a conexão com o banco de dados.
    """
    status = {
        "api": "online",
        "hostname": socket.gethostname(),
        "database": "disconnected"
    }
    
    try:
        db = next(get_db())
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        db.close()
        status["database"] = "connected"
    except Exception as e:
        status["database_error"] = str(e)
    
    return status

@app.post("/upload", response_model=UploadResponse)
async def upload_imagem(db: Session = Depends(get_db)):
    """
    Busca uma imagem aleatória da API pública Dog CEO e salva no banco.
    Retorna a URL da imagem e a tag 'dog'.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://dog.ceo/api/breeds/image/random")
            response.raise_for_status()
            data = response.json()
            
            if data["status"] != "success":
                raise HTTPException(status_code=500, detail="Erro ao buscar imagem da API")
            
            image_url = data["message"]
            tag = "dog"
            
            nova_imagem = Imagem(url=image_url, tag=tag)
            db.add(nova_imagem)
            db.commit()
            db.refresh(nova_imagem)
            
            return {
                "message": "Imagem salva com sucesso",
                "id": nova_imagem.id,
                "url": nova_imagem.url,
                "tag": nova_imagem.tag
            }
    
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar com a API pública: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar imagem: {str(e)}")

@app.get("/listar", response_model=TagResponse)
def listar_tags(db: Session = Depends(get_db)):
    """
    Lista todas as tags únicas que estão armazenadas no banco de dados.
    """
    try:
        tags = db.query(Imagem.tag).distinct().all()
        tags_list = [tag[0] for tag in tags]
        
        return {"tags": tags_list}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar tags: {str(e)}")

@app.get("/mostrar/{id}", response_model=ImagemResponse)
def mostrar_imagem(id: int, db: Session = Depends(get_db)):
    """
    Retorna a URL da imagem correspondente ao ID informado.
    """
    try:
        imagem = db.query(Imagem).filter(Imagem.id == id).first()
        
        if not imagem:
            raise HTTPException(status_code=404, detail=f"Imagem com ID {id} não encontrada")
        
        return imagem
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar imagem: {str(e)}")

@app.get("/imagens", response_model=List[ImagemResponse])
def listar_imagens(db: Session = Depends(get_db)):
    """
    Lista todas as imagens armazenadas no banco de dados.
    """
    try:
        imagens = db.query(Imagem).all()
        return imagens
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar imagens: {str(e)}")

