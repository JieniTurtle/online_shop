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
                    "SELECT product_id, item_code FROM product"
                )
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"get products by category failed: {e}")
            return []
        
    @staticmethod
    def get_product_by_id(product_id):
        try:
            with get_db_cursor() as cursor:
                cursor.execute(
                    "SELECT item_code, category_id, blade_material_id, fittings_material_id, total_length, blade_length, tsuka_length FROM product WHERE product_id = %s",
                    (product_id,)
                )
                result = cursor.fetchone()
                print("get_product_by_id in repository: ", result)
                return result
        except Exception as e:
            print(f"get product by id failed: {e}")
            return []
        
    @staticmethod
    def insert_main_image_url(product_id, image_url):
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(
                    "UPDATE product SET main_image_url = %s WHERE product_id = %s",
                    (image_url, product_id)
                )
            return True
        except Exception as e:
            print(f"insert product main image failed: {e}")
            return False

    @staticmethod
    def get_main_image_url(product_id):
        try:
            with get_db_cursor() as cursor:
                cursor.execute(
                    "SELECT main_image_url FROM product WHERE product_id = %s",
                    (product_id,)
                )
                result = cursor.fetchone()
                return result['main_image_url']
        except Exception as e:
            print(f"get product main image url failed: {e}")