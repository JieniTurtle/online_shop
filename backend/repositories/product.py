from database import get_db_cursor

class Product:
    @staticmethod
    def insert(item_code, category_id, blade_material_id, fittings_material_id, total_length, blade_length, tsuka_length):
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(
                    "INSERT INTO product (item_code, category_id, blade_material_id, fittings_material_id, total_length, blade_length, tsuka_length, main_image_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING product_id",
                    (item_code, category_id, blade_material_id, fittings_material_id, total_length, blade_length, tsuka_length, 'do_it_later')
                    )
                result = cursor.fetchone()
                return result['product_id'] if result else None
            return product_id
        except Exception as e:
            print(f"insert product failed: {e}")
            return False
         
        
    @staticmethod
    def insert_product_description(product_id, description, language):
        if product_id is False:
            return False
        
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(
                    "INSERT INTO description (product_id, content, language_code) VALUES (%s, %s, %s)",
                    (product_id, description, language)
                )
            return True
        except Exception as e:
            print(f"insert product description failed: {e}")
            return False
        
    @staticmethod
    def get_all_item_codes():
        try:
            with get_db_cursor() as cursor:
                cursor.execute(
                    "SELECT item_code FROM product"
                )
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"get products by category failed: {e}")
            return []

        