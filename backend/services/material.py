from repositories.material import Material

class MaterialService:
    @staticmethod
    def get_or_create_material(name, language):
        material_id = Material.get_material_id_by_name(name, language)
        if material_id == -1:
            material_id = Material.create_material()
            Material.insert_material_name(material_id, name, language)
        return material_id
    
    @staticmethod
    def get_material_name(material_id, language):
        return Material.get_material_name(material_id, language)