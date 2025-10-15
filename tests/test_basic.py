from fastapi.testclient import TestClient
from app.main import app
from app.db import init_db
from app.seed_data import seed_all

client = TestClient(app)

def test_docs():
    init_db()
    seed_all()
    r = client.get("/docs")
    assert r.status_code == 200

def test_list_npcs():
    r = client.get("/npcs/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
