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
    UPLOAD_FOLDER = '../frontend/public/images'
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
        image_url = f"/images/{unique_filename}"
        
        # Update product with image URL in database
        result = ProductService.insert_main_image_url(int(product_id), image_url)
        
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

@product_bp.route('/get_detailed_images/<product_id>', methods=['GET'])
def get_detailed_images(product_id):
    return jsonify(ProductService.get_detailed_images(product_id))

@product_bp.route('/upload_detailed_image/<product_id>/<int:order_number>', methods=['POST'])
def upload_detailed_image(product_id, order_number):
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    # Define upload folder
    UPLOAD_FOLDER = '../frontend/public/images'
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
        image_url = f"/images/{unique_filename}"
        
        # Use the correct service method for inserting detailed images
        result = ProductService.insert_detailed_image(int(product_id), image_url, int(order_number))
        
        if result:
            return jsonify({
                'success': True,
                'imageUrl': image_url,
                'message': 'Detailed image uploaded successfully'
            })
        else:
            return jsonify({'error': 'Failed to insert detailed image into database'}), 500
    else:
        return jsonify({'error': 'Invalid file type. Only PNG, JPG, JPEG, GIF allowed.'}), 400
    
@product_bp.route('/delete_detailed_image/<int:image_id>', methods=['DELETE'])  # Changed to DELETE method
def delete_detailed_image(image_id):
    result = ProductService.delete_image(int(image_id))
    if result:
        return jsonify({'success': True, 'message': 'Image deleted successfully'})
    else:
        return jsonify({'error': 'Failed to delete image'}), 500
    

@product_bp.route('/upload_product_table', methods=['POST'])
def upload_product_table():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # 定义上传目录
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'xls', 'xlsx'}
    
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    if file and allowed_file(file.filename):
        # 创建上传目录（如果不存在）
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # 生成唯一文件名
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # 保存文件
        file.save(filepath)
        
        try:
            # 调用服务层方法导入产品数据
            print("file path: ", filepath)
            result = ProductService.insert_product_by_table(filepath)
            print("results: ", result)
            if result:
                return jsonify({
                    'success': True,
                    'message': f'Successfully imported {result} products from table'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Failed to import products from table'
                }), 500
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Error importing products: {str(e)}'
            }), 500
        finally:
            # 可选：删除临时上传的文件
            # os.remove(filepath)
            pass
    else:
        return jsonify({'error': 'Invalid file type. Only XLS, XLSX files allowed.'}), 400