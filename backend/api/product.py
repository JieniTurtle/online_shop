from flask import Blueprint, jsonify, request
from services.product import ProductService
import os
from werkzeug.utils import secure_filename
import uuid

product_bp = Blueprint('product', __name__, url_prefix='/api/product')

@product_bp.route('/get_all_item_codes', methods=['GET'])
def get_all_item_codes():
    return jsonify(ProductService.get_all_item_codes())

@product_bp.route('/get_product_by_id/<product_id>/<language>', methods=['GET'])
def get_product_by_id(product_id, language):
    return jsonify(ProductService.get_product_by_id(product_id, language))

@product_bp.route('/upload_product_image/<product_id>', methods=['POST'])
def upload_product_image(product_id):
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    # Define upload folder
    UPLOAD_FOLDER = 'static/images'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    if file and allowed_file(file.filename):
        # Create upload directory if it doesn't exist
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Save file
        file.save(filepath)
        image_url = f"/static/images/{unique_filename}"
        
        # Update product with image URL in database
        print(int(product_id), image_url)
        result = ProductService.insert_main_image_url(int(product_id), image_url)
        print("result", result)
        
        if result:
            return jsonify({
                'success': True,
                'imageUrl': image_url,
                'message': 'Image uploaded successfully'
            })
        else:
            return jsonify({'error': 'Failed to update product with image URL'}), 500
    else:
        return jsonify({'error': 'Invalid file type. Only PNG, JPG, JPEG, GIF allowed.'}), 400

@product_bp.route('/get_main_image_url/<product_id>', methods=['GET'])
def get_main_image_url(product_id):
    return jsonify(ProductService.get_main_image_url(product_id))