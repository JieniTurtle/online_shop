from repositories.product import Product
from services.category import CategoryService
from services.material import MaterialService
from utils.process_table import get_product_description, get_length_and_material

import pandas as pd

class ProductService:
    @staticmethod
    def insert_product(item_code, category, blade_material, fittings_material, total_length, blade_length, tsuka_length, language):
        category_id = CategoryService.get_or_create_category(category, language)
        blade_material_id = MaterialService.get_or_create_material(blade_material, language)
        fittings_material_id = MaterialService.get_or_create_material(fittings_material, language)
        product_id = Product.insert(item_code, category_id, blade_material_id, fittings_material_id, total_length, blade_length, tsuka_length)
        return product_id

    @staticmethod
    def insert_product_description(product_id, description, language):
        Product.insert_product_description(product_id, description, language)

    @staticmethod
    def insert_product_by_table(file_path):
        try:
            # Read the Excel file
            df = pd.read_excel(file_path)
            
            results = []
            # Iterate through each row
            for index, row in df.iterrows():
                try:
                    # Extract values from the row - adjust column names as needed
                    item_code = row['货号']
                    category = "others"
                    total_length, blade_length, tsuka_length, blade_material, fittings_material \
                        = get_length_and_material(row['规格'])
                    Chinese_description, English_description = get_product_description(row['说明'])
                    
                    # Insert the product
                    product_id = ProductService.insert_product(
                        item_code, category, blade_material, fittings_material,
                        total_length, blade_length, tsuka_length, 'en'
                    )

                    ProductService.insert_product_description(product_id, Chinese_description, 'cn')
                    ProductService.insert_product_description(product_id, English_description, 'en')
                    
                except Exception as e:
                    print(f"Error processing row {index}: {e}")
            
            return results
            
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return []
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return []

    def get_all_item_codes():
        return Product.get_all_item_codes()
    
    def get_product_by_id(product_id, language):
        print("get_product_by_id: product_id=", product_id)
        result = Product.get_product_by_id(product_id)
        print("raw result from Product.get_product_by_id:", result)
        
        if not result:
            raise ValueError(f"Product with id {product_id} not found")
        
        # Access the values from the RealDictRow dictionary
        item_code = result['item_code']
        category_id = result['category_id']
        blade_material_id = result['blade_material_id']
        fittings_material_id = result['fittings_material_id']
        total_length = result['total_length']
        blade_length = result['blade_length']
        tsuka_length = result['tsuka_length']
        print("result:", item_code, category_id, blade_material_id, fittings_material_id, \
            total_length, blade_length, tsuka_length)
        
        category = CategoryService.get_category_name(category_id, language)
        blade_material = MaterialService.get_material_name(blade_material_id, language)
        fittings_material = MaterialService.get_material_name(fittings_material_id, language)

        return {
            'product_id': product_id,
            'item_code': item_code,
            'category': category,
            'blade_material': blade_material,
            'fittings_material': fittings_material,
            'total_length': float(total_length) if total_length else None,
            'blade_length': float(blade_length) if blade_length else None,
            'tsuka_length': float(tsuka_length) if tsuka_length else None
        }
    
    def insert_main_image_url(product_id, image_url):
        return Product.insert_main_image_url(product_id, image_url)

    def get_main_image_url(product_id):
      return Product.get_main_image_url(product_id)
    
import os
from werkzeug.utils import secure_filename
from flask import current_app

# Add these constants at the top of the file (after imports)
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Generate unique filename to prevent conflicts
        import uuid
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Ensure upload directory exists
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        file.save(filepath)
        return f"/static/images/{unique_filename}"  # Return relative path for web access
    return None

# Add this method to your ProductService class
def upload_product_image(product_id, file):
    # Save the uploaded file
    image_url = save_uploaded_file(file)
    if image_url:
        # Update the product record with the image URL
        return ProductService.insert_main_image_url(product_id, image_url)
    return False