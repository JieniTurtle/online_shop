from repositories.category import Category

class CategoryService:
    @staticmethod
    def get_or_create_category(name, language):
        category_id = Category.get_category_id_by_name(name, language)
        if category_id == -1:
            category_id = Category.create_category()
            Category.insert_category_name(category_id, name, language)
        return category_id