from flask import Flask, request, jsonify
from models import db, User, Merchant
import config

app = Flask(__name__)
app.config.from_object(config.Config)
db.init_app(app)

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(
        student_number=data['student_number'],
        pwd=data['pwd'],
        name=data['name'],
        sex=data['sex'],
        BirthDate=data['BirthDate']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added successfully!"})

@app.route('/get_users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.as_dict() for user in users])

@app.route('/update_user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)
    if user:
        user.student_number = data.get('student_number', user.student_number)
        user.pwd = data.get('pwd', user.pwd)
        user.name = data.get('name', user.name)
        user.sex = data.get('sex', user.sex)
        user.BirthDate = data.get('BirthDate', user.BirthDate)
        db.session.commit()
        return jsonify({"message": "User updated successfully!"})
    return jsonify({"message": "User not found!"}), 404

@app.route('/delete_user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully!"})
    return jsonify({"message": "User not found!"}), 404

@app.route('/add_merchant', methods=['POST'])
def add_merchant():
    data = request.get_json()
    new_merchant = Merchant(
        merchant_name=data['merchant_name'],
        contact_number=data['contact_number'],
        address=data['address']
    )
    db.session.add(new_merchant)
    db.session.commit()
    return jsonify({"message": "Merchant added successfully!"})

@app.route('/get_merchants', methods=['GET'])
def get_merchants():
    merchants = Merchant.query.all()
    return jsonify([merchant.as_dict() for merchant in merchants])

@app.route('/update_merchant/<int:id>', methods=['PUT'])
def update_merchant(id):
    data = request.get_json()
    merchant = Merchant.query.get(id)
    if merchant:
        merchant.merchant_name = data.get('merchant_name', merchant.merchant_name)
        merchant.contact_number = data.get('contact_number', merchant.contact_number)
        merchant.address = data.get('address', merchant.address)
        db.session.commit()
        return jsonify({"message": "Merchant updated successfully!"})
    return jsonify({"message": "Merchant not found!"}), 404

@app.route('/delete_merchant/<int:id>', methods=['DELETE'])
def delete_merchant(id):
    merchant = Merchant.query.get(id)
    if merchant:
        db.session.delete(merchant)
        db.session.commit()
        return jsonify({"message": "Merchant deleted successfully!"})
    return jsonify({"message": "Merchant not found!"}), 404

if __name__ == '__main__':
    app.run(debug=True)
