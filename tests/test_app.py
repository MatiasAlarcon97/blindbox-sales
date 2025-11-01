from app.app import app
import json

def test_root():
    client = app.test_client()
    r = client.get("/")
    assert r.status_code == 200
    data = r.get_json()
    assert data["status"] == "ok"

def test_list_products():
    client = app.test_client()
    r = client.get("/products")
    assert r.status_code == 200
    data = r.get_json()
    assert "products" in data
    assert isinstance(data["products"], list)

def test_buy_and_order_flow():
    client = app.test_client()
    # obtener primer producto
    r = client.get("/products")
    prod = r.get_json()["products"][0]
    pid = prod["id"]
    # comprar 1 unidad
    r2 = client.post("/buy", json={"product_id": pid, "quantity": 1, "buyer": "test"})
    assert r2.status_code == 201
    order = r2.get_json()
    assert order["product_id"] == pid
    # listar orders incluye la orden
    r3 = client.get("/orders")
    assert r3.status_code == 200
    orders = r3.get_json()["orders"]
    assert any(o["order_id"] == order["order_id"] for o in orders)
