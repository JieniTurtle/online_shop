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
                        total_length, blade_length, tsuka_length, 'en-US'
                    )

                    ProductService.insert_product_description(product_id, Chinese_description, 'zh-CN')
                    ProductService.insert_product_description(product_id, English_description, 'en-US')
                    
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