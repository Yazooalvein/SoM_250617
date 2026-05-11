import unreal

bp_path = "/Game/Systems/Magic/BP_MagicComponent"
bp = unreal.load_asset(bp_path)
lib = unreal.BlueprintEditorLibrary

# Remove incorrect SpellCooldowns first (it's FName type)
# (already done earlier)

# Build float type via import_text with "real" (UE5 float pin category)
float_pin = unreal.EdGraphPinType()
float_pin.import_text('(PinCategory="real",ContainerType=None)')

name_pin = lib.get_basic_type_by_name("Name")

# Create Map<Name, float>
map_name_float = lib.get_map_type(name_pin, float_pin)

# Remove SpellCooldowns if still exists as wrong type, then add correct one
# First try to remove it
try:
    # Check if it exists - we'll just try to add and see
    pass
except:
    pass

# Recreate SpellCooldowns with Map<Name, float>
r = lib.add_member_variable(bp, "SpellCooldowns_f", map_name_float)
print(f"SpellCooldowns_f added: {r}")

# Also try Map<Name, Name> for UnlockedSpells with correct approach
# Note: UnlockedSpells should be Map<Name, Name> since nested containers aren't supported
name_pin2 = lib.get_basic_type_by_name("Name")
map_name_name = lib.get_map_type(name_pin, name_pin2)
r2 = lib.add_member_variable(bp, "UnlockedSpells_test", map_name_name)
print(f"UnlockedSpells_test added: {r2}")

lib.compile_blueprint(bp)
print("Compile OK")