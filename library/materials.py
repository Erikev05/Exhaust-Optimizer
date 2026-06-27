materials_DB = {
    "Steel": {
        "Density": None,
        "Specific heat": None, 
        "Thermal conductivity": None,
    },
    "Aluminium": {
        "Density": None,
        "Specific heat": None, 
        "Thermal conductivity": None,
    },
    "Stainless Steel": {
        "Density": None,
        "Specific heat": None, 
        "Thermal conductivity": None,
    }

}

def get_all_material_names():
    return list(materials_DB.keys())