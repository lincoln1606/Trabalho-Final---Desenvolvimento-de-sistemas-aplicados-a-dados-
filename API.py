from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import uuid
from typing import Dict

app = FastAPI(
    title="API de Tarefas (To-Do List)",
    description="API para gerenciar uma lista de tarefas.",
    version="1.0.0"
)


class Tarefa(BaseModel):
    titulo: str = Field(..., min_length=3)
    descricao: str | None = None
    concluida: bool = False

# Banco de dados em memória
db_tarefas: Dict[str, Tarefa] = {}



@app.post("/tarefas", status_code=status.HTTP_201_CREATED)
def criar_tarefa(tarefa: Tarefa):
    """Cria uma nova tarefa."""
    id_tarefa = str(uuid.uuid4())
    db_tarefas[id_tarefa] = tarefa
    return {"id": id_tarefa, "tarefa": tarefa}

@app.get("/tarefas")
def listar_tarefas():
    """Lista todas as tarefas."""
    return [{"id": id, "tarefa": t} for id, t in db_tarefas.items()]

@app.get("/tarefas/{id}")
def obter_tarefa(id: str):
    """Retorna uma tarefa específica."""
    if id not in db_tarefas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")
    
    return {"id": id, "tarefa": db_tarefas[id]}

@app.put("/tarefas/{id}")
def atualizar_tarefa(id: str, tarefa: Tarefa):
    """Atualiza uma tarefa existente."""
    if id not in db_tarefas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")
    
    db_tarefas[id] = tarefa
    return {"id": id, "tarefa": tarefa}

@app.delete("/tarefas/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_tarefa(id: str):
    """Deleta uma tarefa."""
    if id not in db_tarefas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")
    
    del db_tarefas[id]
    return
