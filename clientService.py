import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

USER_SERVICE_URL = 'http://localhost:5000/users'
ORDER_SERVICE_URL = 'http://localhost:5001/orders'
PRODUCT_SERVICE_URL = 'http://localhost:5002/products'

@app.route('/user-orders/<user_id>', methods=['GET'])
def get_user_order_details(user_id):
    # Fetch user details
    user_response = requests.get(f"{USER_SERVICE_URL}/{user_id}")
    if user_response.status_code != 200:
        return jsonify({"error": "User not found"}), 404
    user_data = user_response.json()

    # Fetch orders for the user
    order_response = requests.get(f"{ORDER_SERVICE_URL}", params={"user_id": user_id})
    order_data = order_response.json()

    # Fetch product details for each order
    for order in order_data:
        product_id = order["product_id"]
        product_response = requests.get(f"{PRODUCT_SERVICE_URL}/{product_id}")
        if product_response.status_code == 200:
            order["product_details"] = product_response.json()

    # Consolidate data
    response_data = {
        "user": user_data,
        "orders": order_data
    }
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(port=5003)
