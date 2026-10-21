# ============================================================
# seguranca.py — Verificação do token JWT
# Descrição: Função usada pelas rotas protegidas para conferir
#            se quem está fazendo a requisição tem um token válido.
# ============================================================

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITMO = "HS256"

# HTTPBearer() é o que faz o botão "Authorize" aparecer no /docs
esquema_token = HTTPBearer()

# "Segurança de porta" — confere se o token que veio na requisição é válido
def verificar_token(credenciais: HTTPAuthorizationCredentials = Depends(esquema_token)):
    token = credenciais.credentials   # o texto do token, sem a palavra "Bearer" na frente

    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITMO])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado, faça login de novo")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


def verificar_admin(payload: dict = Depends(verificar_token)):
    if payload.get("tipo") != "admin":
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores")
    return payload