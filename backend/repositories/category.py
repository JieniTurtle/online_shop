from database import get_db_cursor

class Category:
    @staticmethod
    def get_category_id_by_name(name, language):
        if language not in ["zh-CN", "en-US"]:
            print("Invalid language {language}, check the spelling")
            return -1
        
        try:
            with get_db_cursor() as cursor:
                cursor.execute(
                    "SELECT category_id FROM category_name WHERE name = %s AND language_code = %s",
                    (name, language)
                )
                result = cursor.fetchone()
                return result['category_id'] if result else None
        except Exception as e:
            print(f"get_category_id_by_name query failed: {e}")
            return -1

    @staticmethod
    def create_category():
        try:
            with get_db_cursor() as cursor:
                cursor.execute(
                    "INSERT INTO category DEFAULT VALUES RETURNING category_id"
                )
                result = cursor.fetchone()
                return result['category_id'] if result else None
        except Exception as e:
            print(f"create_category query failed: {e}")
            return -1

    @staticmethod
    def insert_category_name(category_id, name, language):
        if language not in ["zh-CN", "en-US"]:
            print("Invalid language {language}, check the spelling")
            return False
        
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(
                    "INSERT INTO category_name (category_id, name, language_code) VALUES (%s, %s, %s)",
                    (category_id, name, language)
                )
                return True
        except Exception as e:
            print(f"insert_category_name query failed: {e}")
            return False
    