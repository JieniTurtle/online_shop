from repositories.category import Category

class CategoryService:
    @staticmethod
    def get_or_create_category(name, language):
        category_id = Category.get_category_id_by_name(name, language)
        print("category_id", category_id)
        if category_id == None:
            category_id = Category.create_category()
            print("created category_id ", category_id)
            Category.insert_category_name(category_id, name, language)
        return category_id
    
    @staticmethod
    def get_category_name(category_id, language):
        return Category.get_category_name(category_id, language)