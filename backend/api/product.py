from flask import Blueprint, jsonify, request
from services.product import ProductService


product_bp = Blueprint('product', __name__, url_prefix='/api/product')

@product_bp.route('/get_all_item_codes', methods=['GET'])
def get_all_item_codes():
    return jsonify(ProductService.get_all_item_codes())