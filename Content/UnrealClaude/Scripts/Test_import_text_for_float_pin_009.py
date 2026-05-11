import unreal

lib = unreal.BlueprintEditorLibrary

# Try import_text to set pin type from serialized string
test_formats = [
    '(PinCategory="real",ContainerType=None)',
    '(PinCategory="real",PinSubCategory="",ContainerType=None,bIsReference=False)',
    '(PinCategory="float",ContainerType=None)',
    '(PinCategory="double",ContainerType=None)',
    '(PinCategory="real")',
]

for fmt in test_formats:
    try:
        pin = unreal.EdGraphPinType()
        pin.import_text(fmt)
        print(f"OK: {fmt}")
        # Try to use it
        name_pin = lib.get_basic_type_by_name("Name")
        map_pin = lib.get_map_type(name_pin, pin)
        print(f"  Map tuple: {map_pin.to_tuple()}")
    except Exception as e:
        print(f"FAIL '{fmt}': {e}")

# Also try accessing the TestFloat variable via the generated class CDO
bp = unreal.load_asset("/Game/Systems/Magic/BP_MagicComponent")
cdo = bp.generated_class().get_default_object()
try:
    v = cdo.get_editor_property("TestFloat")
    print(f"\nTestFloat value: {v}, type: {type(v)}")
except Exception as e:
    print(f"\nCDO TestFloat: {e}")