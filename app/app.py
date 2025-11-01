from flask import Flask, jsonify, request
import uuid
from datetime import datetime

app = Flask(__name__)

# "DB" en memoria
PRODUCTS = [
    {"id": "p1", "name": "Blindbox - Figura A", "price": 25.0, "stock": 10},
    {"id": "p2", "name": "Blindbox - Figura B", "price": 30.0, "stock": 8},
    {"id": "p3", "name": "Blindbox - Figura C", "price": 20.0, "stock": 15},
]
ORDERS = []

@app.route("/")
def root():
    return jsonify({"status": "ok", "service": "blindbox-sales", "version": "0.1"})

@app.route("/products", methods=["GET"])
def list_products():
    return jsonify({"products": PRODUCTS})

@app.route("/products/<product_id>", methods=["GET"])
def get_product(product_id):
    prod = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not prod:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify(prod)

@app.route("/buy", methods=["POST"])
def buy():
    data = request.get_json() or {}
    product_id = data.get("product_id")
    quantity = int(data.get("quantity", 1))
    buyer = data.get("buyer", "guest")

    prod = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not prod:
        return jsonify({"error": "Producto no encontrado"}), 404
    if prod["stock"] < quantity:
        return jsonify({"error": "Stock insuficiente"}), 400

    prod["stock"] -= quantity

    order = {
        "order_id": str(uuid.uuid4()),
        "product_id": product_id,
        "quantity": quantity,
        "buyer": buyer,
        "total": round(prod["price"] * quantity, 2),
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    ORDERS.append(order)
    return jsonify(order), 201

@app.route("/orders", methods=["GET"])
def list_orders():
    return jsonify({"orders": ORDERS})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
