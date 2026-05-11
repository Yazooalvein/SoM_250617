import unreal
print('BlueprintEditorLibrary:', hasattr(unreal, 'BlueprintEditorLibrary'))
bp = unreal.load_asset('/Game/Systems/Magic/BP_MagicComponent')
print(f'BP: {bp.get_name()}')
pin = unreal.EdGraphPinType()
print('EdGraphPinType OK')
print([x for x in dir(pin) if not x.startswith('_')])