# ============================================================
# rotas/agendamentos.py — CRUD de Agendamentos
# Descrição: Endpoints para gerenciar os agendamentos de sessões
#            de tatuagem. Cada agendamento liga um cliente a um
#            tatuador (duas chaves estrangeiras).
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from database import conectar

router = APIRouter()

# Modelo de dados — define os campos que o agendamento deve ter
class Agendamento(BaseModel):
    idcliente: int                          # obrigatório — aponta para a tabela cliente
    idtatuador: int                         # obrigatório — aponta para a tabela tatuador
    dataagendamento: str                    # obrigatório
    horaagendamento: str                    # obrigatório
    descricaotatuagem: Optional[str] = None # opcional
    valortatuagem: Optional[float] = None   # opcional
    status: Optional[str] = None            # só é usado ao atualizar (ver Parte 7)

@router.post("/agendamentos")
def criar_agendamento(agendamento: Agendamento):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO agendamento (idcliente, idtatuador, dataagendamento, horaagendamento, descricaotatuagem, valortatuagem)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (agendamento.idcliente, agendamento.idtatuador, agendamento.dataagendamento,
         agendamento.horaagendamento, agendamento.descricaotatuagem, agendamento.valortatuagem)
    )
    # repare que a coluna status nem aparece aqui — o banco aplica sozinho
    # o DEFAULT 'pendente' que já foi definido lá na Aula 2
    conn.commit()
    conn.close()
    return {"mensagem": "Agendamento cadastrado com sucesso"}