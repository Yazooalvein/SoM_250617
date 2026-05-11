import unreal

bp_path = "/Game/Systems/Magic/BP_MagicComponent"
bp = unreal.load_asset(bp_path)
lib = unreal.BlueprintEditorLibrary

name_type = lib.get_basic_type_by_name("Name")
float_type = lib.get_basic_type_by_name("float")

# SpellCooldowns: Map<Name, float>
map_name_float = lib.get_map_type(name_type, float_type)
r1 = lib.add_member_variable(bp, "SpellCooldowns", map_name_float)
print(f"SpellCooldowns Map<Name,float>: {r1}")

# UnlockedSpells: Map<Name, Name>
# (BP ne supporte pas Map<Name, Array<Name>> sans struct intermediaire)
map_name_name = lib.get_map_type(name_type, name_type)
r2 = lib.add_member_variable(bp, "UnlockedSpells", map_name_name)
print(f"UnlockedSpells Map<Name,Name>: {r2}")
lib.set_blueprint_variable_instance_editable(bp, "UnlockedSpells", True)

lib.compile_blueprint(bp)
print("Compile OK")