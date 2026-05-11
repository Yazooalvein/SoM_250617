import unreal

bp_path = "/Game/Systems/Magic/BP_MagicComponent"
bp = unreal.load_asset(bp_path)
lib = unreal.BlueprintEditorLibrary

# Inspect new_variables to find the float pin type
try:
    new_vars = bp.get_editor_property("new_variables")
    print(f"new_variables count: {len(new_vars)}")
    for vd in new_vars:
        name = vd.get_editor_property("var_name")
        vtype = vd.get_editor_property("variable_type")
        print(f"  {name}: type tuple = {vtype.to_tuple()}")
        if "TestFloat" in str(name) or "float" in str(name).lower():
            print(f"  -> Float pin type found!")
            # Try to use this as value type in get_map_type
            name_type = lib.get_basic_type_by_name("Name")
            map_type = lib.get_map_type(name_type, vtype)
            print(f"  -> Map<Name, float> tuple: {map_type.to_tuple()}")
except Exception as e:
    print(f"Error accessing new_variables: {e}")