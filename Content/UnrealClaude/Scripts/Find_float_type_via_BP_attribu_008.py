import unreal

bp = unreal.load_asset("/Game/Systems/Magic/BP_MagicComponent")
lib = unreal.BlueprintEditorLibrary

# Try to access Blueprint properties differently
print("bp type:", type(bp))
props = [p for p in dir(bp) if not p.startswith("_")]
print("BP properties:", props[:30])

# Try variables_desc
for attr in ["variables_desc", "member_variables", "variable_guids", "variable_data", "new_variable_data"]:
    try:
        v = bp.get_editor_property(attr)
        print(f"bp.{attr} = {v}")
    except:
        pass

# Check if we can find a float variable node in the event graph
try:
    graph = lib.find_event_graph(bp)
    print("Event graph found:", graph)
    nodes = [n for n in dir(graph) if not n.startswith("_")]
    print("Graph attrs:", nodes[:20])
except Exception as e:
    print(f"Graph error: {e}")