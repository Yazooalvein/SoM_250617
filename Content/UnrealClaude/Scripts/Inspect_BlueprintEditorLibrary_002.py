import unreal
lib = unreal.BlueprintEditorLibrary
print('BlueprintEditorLibrary methods:')
for m in sorted(dir(lib)):
    if not m.startswith('_'):
        print(' ', m)
pin = unreal.EdGraphPinType()
print('
EdGraphPinType properties via get_editor_property:')
try:
    for prop in ['pin_category','pin_sub_category','container_type','is_map_value_pin_type','pin_value_type']:
        try:
            v = pin.get_editor_property(prop)
            print(f'  {prop} = {v}')
        except Exception as e:
            print(f'  {prop}: ERROR {e}')
except Exception as e:
    print(f'outer error: {e}')