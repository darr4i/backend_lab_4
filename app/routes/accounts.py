from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import db, Account

account_bp = Blueprint('accounts', __name__, url_prefix='/accounts')

@account_bp.route('/', methods=['POST'])
def create_account():
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    account = Account(user_id=user_id)
    db.session.add(account)
    db.session.commit()

    return jsonify({"message": "Account created successfully", "account_id": account.id}), 201

@account_bp.route('/<int:account_id>', methods=['GET'])
@jwt_required()
def get_account(account_id):
    account = Account.query.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    return jsonify({
        "account_id": account.id,
        "user_id": account.user_id,
        "balance": account.balance
    }), 200

@account_bp.route('/<int:account_id>/balance', methods=['PATCH'])
@jwt_required()
def update_balance(account_id):
    data = request.get_json()
    amount = data.get("amount")

    if not amount or amount <= 0:
        return jsonify({"error": "Amount must be greater than 0"}), 400

    account = Account.query.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    account.balance += amount
    db.session.commit()

    return jsonify({"message": "Balance updated successfully", "new_balance": account.balance}), 200
