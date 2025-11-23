from fastapi.testclient import TestClient
from main import app, db_tarefas

client = TestClient(app)


def test_criar_tarefa_sucesso():
    resposta = client.post("/tarefas", json={"titulo": "Estudar", "descricao": "Ler capítulo 3"})
    assert resposta.status_code == 201
    dados = resposta.json()
    assert "id" in dados
    assert dados["tarefa"]["titulo"] == "Estudar"

def test_criar_tarefa_sem_titulo():
    resposta = client.post("/tarefas", json={"titulo": ""})
    assert resposta.status_code in (400, 422)


def test_listar_tarefas_vazio():
    db_tarefas.clear()
    resposta = client.get("/tarefas")
    assert resposta.status_code == 200
    assert resposta.json() == []

def test_listar_tarefas_com_itens():
    client.post("/tarefas", json={"titulo": "Tarefa 1"})
    resposta = client.get("/tarefas")
    assert resposta.status_code == 200
    assert len(resposta.json()) >= 1


def test_buscar_tarefa_por_id():
    res = client.post("/tarefas", json={"titulo": "Nova"})
    id_tarefa = res.json()["id"]

    resposta = client.get(f"/tarefas/{id_tarefa}")
    assert resposta.status_code == 200
    assert resposta.json()["tarefa"]["titulo"] == "Nova"

def test_buscar_tarefa_id_inexistente():
    resposta = client.get("/tarefas/nao_existe")
    assert resposta.status_code == 404



def test_atualizar_tarefa_sucesso():
    res = client.post("/tarefas", json={"titulo": "Antigo"})
    id_tarefa = res.json()["id"]

    resposta = client.put(f"/tarefas/{id_tarefa}", json={
        "titulo": "Atualizado",
        "descricao": "Novo texto",
        "concluida": True
    })

    assert resposta.status_code == 200
    assert resposta.json()["tarefa"]["titulo"] == "Atualizado"

def test_atualizar_tarefa_inexistente():
    resposta = client.put("/tarefas/nao_existe", json={
        "titulo": "X",
        "descricao": "Y",
        "concluida": False
    })
    assert resposta.status_code == 404



def test_deletar_tarefa_sucesso():
    res = client.post("/tarefas", json={"titulo": "Apagar"})
    id_tarefa = res.json()["id"]

    resposta = client.delete(f"/tarefas/{id_tarefa}")
    assert resposta.status_code == 204

    resposta2 = client.get(f"/tarefas/{id_tarefa}")
    assert resposta2.status_code == 404

def test_deletar_tarefa_inexistente():
    resposta = client.delete("/tarefas/nao_existe")
    assert resposta.status_code == 404
