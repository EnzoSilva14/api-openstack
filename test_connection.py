"""
Script para testar a conexão com o banco de dados PostgreSQL.
Execute: python test_connection.py
"""

import sys
import socket
from sqlalchemy import create_engine, text

# Configuração do banco
DB_HOST = "192.169.0.84"
DB_PORT = 5432
DB_NAME = "minhadb"
DB_USER = "api_user"
DB_PASSWORD = "senha_forte_123"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

print("=" * 60)
print("TESTE DE CONEXÃO COM BANCO DE DADOS POSTGRESQL")
print("=" * 60)

# 1. Teste de rede básico
print(f"\n1️⃣  Testando conectividade de rede com {DB_HOST}...")
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    result = sock.connect_ex((DB_HOST, DB_PORT))
    sock.close()
    
    if result == 0:
        print(f"   ✅ Porta {DB_PORT} está acessível em {DB_HOST}")
    else:
        print(f"   ❌ Porta {DB_PORT} NÃO está acessível em {DB_HOST}")
        print(f"   Código de erro: {result}")
except Exception as e:
    print(f"   ❌ Erro ao testar rede: {e}")

# 2. Teste de conexão com SQLAlchemy
print(f"\n2️⃣  Testando conexão com SQLAlchemy...")
print(f"   URL: {DATABASE_URL.replace(DB_PASSWORD, '***')}")

try:
    engine = create_engine(DATABASE_URL, connect_args={'connect_timeout': 5})
    connection = engine.connect()
    result = connection.execute(text("SELECT version()"))
    version = result.fetchone()[0]
    connection.close()
    
    print(f"   ✅ Conexão bem-sucedida!")
    print(f"   PostgreSQL version: {version}")
    
except Exception as e:
    print(f"   ❌ Erro ao conectar: {e}")
    print("\n🔍 POSSÍVEIS CAUSAS:")
    print("   • IP incorreto (192.169.0.84 não é um IP privado padrão)")
    print("   • Firewall bloqueando a porta 5432")
    print("   • PostgreSQL não está rodando no servidor")
    print("   • PostgreSQL não aceita conexões externas")
    print("   • Credenciais incorretas")
    print("\n💡 SUGESTÕES:")
    print("   • Verifique se o IP correto não seria 192.168.0.84")
    print("   • Leia o arquivo CONFIGURACAO_BANCO.md para mais detalhes")

# 3. Verificar hostname local
print(f"\n3️⃣  Hostname desta máquina: {socket.gethostname()}")

print("\n" + "=" * 60)
print("Teste concluído!")
print("=" * 60)

