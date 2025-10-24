from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict

# Criando a aplicação FastAPI
app = FastAPI(
    title="API de Cadastro de Alunos",
    description="API para realizar operações de cadastro de alunos (CRUD).",
    version="1.0.0"
)

# Modelo de dados do Aluno
class Aluno(BaseModel):
    nome: str
    turma: str
    idade: int

# "Banco de dados" em memória (dicionário)
db_alunos: Dict[int, Aluno] = {
    1: Aluno(nome="Claudio", turma="2A", idade=16),
    2: Aluno(nome="Luciano", turma="3B", idade=17),
    3: Aluno(nome="Marcos", turma="1C", idade=15),
}

# --- ENDPOINTS ---

@app.get("/")
def raiz():
    return {"message": "Bem-vindo a Api de Alunos!!! Vá até /docs para testar."}

@app.get("/alunos")
def listar_alunos():
    """Lista todos os alunos cadastrados"""
    return db_alunos

@app.get("/alunos/{id}")
def pegar_aluno(id: int):
    """Retorna um aluno pelo id."""
    if id not in db_alunos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")
    return db_alunos[id]

@app.post("/alunos/{id}", status_code=status.HTTP_201_CREATED)
def criar_aluno(id: int, aluno: Aluno):
    """Cria um novo aluno com um id específico."""
    if id in db_alunos:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Já existe um aluno com essa matrícula")
    
    db_alunos[id] = aluno
    return {"message": "Aluno cadastrado com sucesso!", "matrícula": id, "aluno": aluno}

@app.put("/alunos/{id}")
def atualizar_aluno(id: int, aluno: Aluno):
    """Atualiza os dados de um aluno já existente."""
    if id not in db_alunos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")
    
    db_alunos[id] = aluno
    return {"message": "Dados do aluno atualizados com sucesso!", "aluno": aluno}

@app.delete("/alunos/{id}")
def deletar_aluno(id: int):
    """Deleta o cadastro de um aluno pelo id."""
    if id not in db_alunos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")
    
    del db_alunos[id]
    return {"message": "Aluno deletado com sucesso!"}


"""Fiz esta Api em cima do exemplo que o professor pas
