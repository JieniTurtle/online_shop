from database import get_db_cursor

class Material:
    @staticmethod
    def get_material_id_by_name(name, language):
        if language not in ["cn", "en"]:
            print("Invalid language {language}, check the spelling")
            return -1
        
        try:
            with get_db_cursor() as cursor:
                cursor.execute(
                    "SELECT material_id FROM material_name WHERE name = %s AND language_code = %s",
                    (name, language)
                )
                result = cursor.fetchone()  # 在 with 块内获取结果
                if result:
                    return result["material_id"]
                return -1  # 没找到返回 -1
        except Exception as e:
            print(f"get_material_id_by_name query failed: {e}")
            return -1

    @staticmethod
    def create_material():
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(
                    "INSERT INTO material DEFAULT VALUES RETURNING material_id"
                )
                result = cursor.fetchone()
                return result['material_id'] if result else None
        except Exception as e:
            print(f"create_material query failed: {e}")
            return -1

    @staticmethod
    def insert_material_name(material_id, name, language):
        if language not in ["cn", "en"]:
            print("Invalid language {language}, check the spelling")
            return False
        
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(
                    "INSERT INTO material_name (material_id, name, language_code) VALUES (%s, %s, %s)",
                    (material_id, name, language)
                )
                return True
        except Exception as e:
            print(f"insert_material_name query failed: {e}")
            return False
    
    @staticmethod
    def get_material_name(material_id, language):
        try:
            with get_db_cursor() as cursor:
                cursor.execute(
                    "SELECT name FROM material_name WHERE material_id = %s AND language_code = %s",
                    (material_id, language)
                )
                result = cursor.fetchone()
                return result["name"] if result else None
        except Exception as e:
            print(f"get_material_name query failed: {e}")