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


    @staticmethod
    def insert_detailed_image(product_id, image_url, order_number=0):
        """
        插入详细图片
        :param product_id: 产品ID
        :param image_url: 图片URL
        :param order_number: 图片顺序号，默认为0（普通图片，1为主图）
        """
        try:
            with get_db_cursor(commit=True) as cursor:
                # 检查相同产品和顺序号的图片是否已存在
                cursor.execute(
                    "SELECT image_id FROM image WHERE product_id = %s AND order_number = %s",
                    (product_id, order_number)
                )
                existing = cursor.fetchone()
                
                if existing:
                    # 如果已存在，则更新图片URL
                    cursor.execute(
                        "UPDATE image SET url = %s WHERE image_id = %s",
                        (image_url, existing['image_id'])
                    )
                else:
                    # 如果不存在，则插入新图片
                    cursor.execute(
                        "INSERT INTO image (product_id, url, order_number) VALUES (%s, %s, %s)",
                        (product_id, image_url, order_number)
                    )
                    
            return True
        except Exception as e:
            print(f"insert detailed image failed: {e}")
            return False

    @staticmethod
    def get_detailed_images(product_id):
        """
        获取产品所有图片
        :param product_id: 产品ID
        :return: 包含所有图片URL的列表
        """
        try:
            with get_db_cursor() as cursor:
                cursor.execute(
                    "SELECT image_id, url FROM image WHERE product_id = %s ORDER BY order_number ASC",
                    (product_id,)
                )
                results = cursor.fetchall()
                return results
        except Exception as e:
            print(f"get product images failed: {e}")
            return []
        
    @staticmethod
    def get_product_id_and_order(image_id):
        try:
            with get_db_cursor(commit=False) as cursor:
                # 获取要删除的图片信息
                cursor.execute(
                    "SELECT product_id, order_number FROM image WHERE image_id = %s",
                    (image_id,)
                )
                image_info = cursor.fetchone()
                
                if not image_info:
                    print(f"Image with id {image_id} does not exist")
                    return False
                
                product_id = image_info['product_id']
                order_number = image_info['order_number']

                return product_id, order_number
        except Exception as e:
            print(f"delete image failed: {e}")
            return False

    @staticmethod
    def delete_image(image_id):
        """
        删除指定图片，并调整后续图片的order_number以保持连续性
        :param image_id: 图片ID
        """
        try:
            with get_db_cursor(commit=True) as cursor:
                # 删除指定图片
                cursor.execute(
                    "DELETE FROM image WHERE image_id = %s",
                    (image_id,)
                )
        
            return True
        except Exception as e:
            print(f"delete image failed: {e}")
            return False
        
    @staticmethod
    def decrease_order_number(product_id, order_number):
        try:
            with get_db_cursor(commit=True) as cursor:
                # 将同一产品中order_number大于被删除图片的所有图片的order_number减1
                cursor.execute(
                    "UPDATE image SET order_number = order_number - 1 "
                    "WHERE product_id = %s AND order_number > %s",
                    (product_id, order_number)
                )
                
            return True
        except Exception as e:
            print(f"delete image failed: {e}")
            return False