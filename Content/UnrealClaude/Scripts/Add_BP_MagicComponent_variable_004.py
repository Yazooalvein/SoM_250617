import unreal

bp_path = "/Game/Systems/Magic/BP_MagicComponent"
bp = unreal.load_asset(bp_path)
if not bp:
    raise Exception("Cannot load BP_MagicComponent")

lib = unreal.BlueprintEditorLibrary

name_type = lib.get_basic_type_by_name("Name")
float_type = lib.get_basic_type_by_name("Float")
array_name_type = lib.get_array_type(name_type)
map_name_float = lib.get_map_type(name_type, float_type)

print(f"name_type: {name_type.to_tuple()}")
print(f"array_name: {array_name_type.to_tuple()}")
print(f"map_name_float: {map_name_float.to_tuple()}")

try:
    map_name_array = lib.get_map_type(name_type, array_name_type)
    print(f"Map<Name,Array<Name>> supported: {map_name_array.to_tuple()}")
    map_supported = True
except Exception as e:
    print(f"Map<Name,Array<Name>> not supported: {e}")
    map_supported = False

r1 = lib.add_member_variable(bp, "QuickslotSlots", array_name_type)
print(f"QuickslotSlots: {r1}")
lib.set_blueprint_variable_instance_editable(bp, "QuickslotSlots", True)

r2 = lib.add_member_variable(bp, "SpellCooldowns", map_name_float)
print(f"SpellCooldowns: {r2}")

if map_supported:
    r3 = lib.add_member_variable(bp, "UnlockedSpells", map_name_array)
    print(f"UnlockedSpells Map<Name,Array<Name>>: {r3}")
else:
    map_name_name = lib.get_map_type(name_type, name_type)
    r3 = lib.add_member_variable(bp, "UnlockedSpells", map_name_name)
    print(f"UnlockedSpells Map<Name,Name> fallback: {r3}")
lib.set_blueprint_variable_instance_editable(bp, "UnlockedSpells", True)

lib.compile_blueprint(bp)
print("Compile OK")