from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["team_4"]
collection = db["collection_2"]

@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    # Find product by id, exclude MongoDB _id field
    product = list(collection.find({}, {"_id": 0}))[0].get(product_id)
    print(product,"product")
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(port=5002)



