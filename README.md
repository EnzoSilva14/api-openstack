# API de Imagens - FastAPI

API desenvolvida em FastAPI para gerenciar URLs de imagens obtidas de uma API pública.

### Testar Conexão com o Banco

Antes de executar a API, teste a conexão:

```bash
python test_connection.py
```

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute a aplicação:
```bash
uvicorn main:app --host 0.0.0.0 --port 8080
```

A API irá iniciar **mesmo se o banco não estiver disponível**, permitindo testar o endpoint de hostname.

## 🎨 Frontend Web

Após iniciar a API, acesse a interface web em:

### **http://localhost:8080/app** ⬅️ ACESSE AQUI!

O frontend permite:
- ✅ Ver status da API e banco em tempo real
- ✅ Fazer upload de imagens da API pública
- ✅ Listar todas as tags
- ✅ Buscar imagens por ID
- ✅ Visualizar galeria completa de imagens

📖 **Guia completo**: Leia [`COMO_USAR.md`](COMO_USAR.md) para instruções detalhadas

## Endpoints

### GET /
Retorna o hostname da máquina para verificar balanceamento de carga.

**Resposta:**
```json
{
  "hostname": "api1"
}
```

### GET /app
Serve a interface web (frontend) da aplicação.

Acesse no navegador: **http://localhost:8080/app**

### GET /health
Verifica o status da API e a conexão com o banco de dados.

**Resposta (com banco conectado):**
```json
{
  "api": "online",
  "hostname": "DESKTOP-XXXXX",
  "database": "connected"
}
```

**Resposta (sem banco):**
```json
{
  "api": "online",
  "hostname": "DESKTOP-XXXXX",
  "database": "disconnected",
  "database_error": "connection to server at ..."
}
```

### POST /upload
Busca uma imagem aleatória da API pública Dog CEO e salva no banco de dados.

**Resposta:**
```json
{
  "message": "Imagem salva com sucesso",
  "id": 1,
  "url": "https://images.dog.ceo/breeds/hound-afghan/n02088094_1003.jpg",
  "tag": "dog"
}
```

### GET /listar
Lista todas as tags únicas armazenadas no banco de dados.

**Resposta:**
```json
{
  "tags": ["dog"]
}
```

### GET /mostrar/{id}
Retorna a URL da imagem correspondente ao ID informado.

**Resposta:**
```json
{
  "id": 1,
  "url": "https://images.dog.ceo/breeds/hound-afghan/n02088094_1003.jpg",
  "tag": "dog"
}
```

### GET /imagens
Endpoint extra que lista todas as imagens armazenadas (útil para debug).

**Resposta:**
```json
[
  {
    "id": 1,
    "url": "https://images.dog.ceo/breeds/hound-afghan/n02088094_1003.jpg",
    "tag": "dog"
  },
  {
    "id": 2,
    "url": "https://images.dog.ceo/breeds/terrier-american/n02093428_6396.jpg",
    "tag": "dog"
  }
]
```

## Documentação Interativa

Após iniciar o servidor, acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Estrutura do Projeto

```
.
├── main.py                    # Arquivo principal com os endpoints
├── models.py                  # Modelos SQLAlchemy
├── database.py                # Configuração do banco de dados
├── test_connection.py         # Script para testar conexão com o banco
├── requirements.txt           # Dependências do projeto
├── Dockerfile                 # Para containerização
├── README.md                  # Este arquivo
├── CONFIGURACAO_BANCO.md      # Guia de troubleshooting do banco
└── exemplos_requisicoes.md    # Exemplos de uso da API
```

## API Pública Utilizada

Esta aplicação utiliza a [Dog CEO API](https://dog.ceo/dog-api/) que fornece imagens aleatórias de cachorros gratuitamente, sem necessidade de autenticação.
