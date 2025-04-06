from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["team_4"]
collection = db["collection_1"]

@app.route('/orders', methods=['GET'])
def get_orders_by_user():
    user_id = request.args.get('user_id')
    
    # Query MongoDB for orders by user_id
    user_orders = list(collection.find({"user_id": user_id}, {"_id": 0}))  # Exclude _id from result

    return jsonify(user_orders)

if __name__ == '__main__':
    app.run(port=5001)