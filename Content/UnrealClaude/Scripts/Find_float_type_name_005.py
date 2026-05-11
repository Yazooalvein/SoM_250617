import unreal
lib = unreal.BlueprintEditorLibrary

# Try different float type names
for name in ["float", "real", "double", "Float", "REAL", "numeric", "number"]:
    try:
        t = lib.get_basic_type_by_name(name)
        print(f"'{name}' -> {t.to_tuple()}")
    except Exception as e:
        print(f"'{name}' -> ERROR: {e}")

# Also inspect the signature of get_basic_type_by_name
import inspect
try:
    print("\nadd_member_variable sig:", inspect.signature(lib.add_member_variable))
except:
    pass