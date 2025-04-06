from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["team_4"]

users_col = db["collection_3"]
orders_col = db["collection_1"]
products_col = db["collection_2"]

@app.route('/user-orders', methods=['GET'])
def get_user_orders():
    user_id = request.args.get("user_id")

    # Get user info
    user = users_col.find_one({"id": user_id}, {"_id": 0})
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Get orders for this user
    orders = list(orders_col.find({"user_id": user_id}, {"_id": 0}))

    # Enrich orders with product details
    for order in orders:
        product = products_col.find_one({"id": order["product_id"]}, {"_id": 0})
        order["product_details"] = product if product else {}

    return jsonify({
        "user": user,
        "orders": orders
    })

if __name__ == '__main__':
    app.run(port=5000)