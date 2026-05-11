import unreal
lib = unreal.BlueprintEditorLibrary
print('BlueprintEditorLibrary methods:')
for m in sorted(dir(lib)):
    if not m.startswith('_'):
        print(m)
pin = unreal.EdGraphPinType()
for prop in ['pin_category','container_type','is_map_value_pin_type']:
    try:
        print(prop, '=', pin.get_editor_property(prop))
    except Exception as e:
        print(prop, 'ERROR:', e)