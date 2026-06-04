# BP_EssenceDrop -- Snapshot

**Path UE5 :** `/Game/Systems/Essence/BP_EssenceDrop`
**Parent :** Actor
**Noeuds totaux :** 22
**Dernier snapshot :** 05/06/2026 -- Audit global

---

## Composants

- SphereComponent (root, OverlapAllDynamic)
- StaticMeshComponent (NoCollision obligatoire)
- PointLight

## Variables

| Nom | Type | Notes |
|---|---|---|
| EssenceValue | int64 | Valeur a transferer au pickup |
| bCanBePickedUp | bool | Active apres Delay 1.5s en BeginPlay |

## EventGraph

- **BeginPlay :** Delay(1.5s) -> SET bCanBePickedUp=true
- **ActorBeginOverlap :** Branch(bCanBePickedUp) -> Cast HC -> AttributeSetRef -> GetStatValue(EssenceValue) + valeur drop -> SetStatValue(EssenceValue) -> DestroyActor

## Dependances

**Appelle :** BP_AttributeSet_Base (GetStatValue + SetStatValue)
**Spawn par :** BP_SoM_PlayerController (OnHeroDied), BP_Enemy_Base.OnDeath (a implementer -- ENEMY-DropSystem)

## Notes techniques

- StaticMesh NoCollision OBLIGATOIRE (sinon bloque le joueur)
- bCanBePickedUp + Delay 1.5s OBLIGATOIRE (sinon pickup immediat avant que le drop soit visible)
- EssenceValue configurable a la creation (SpawnActor -> SET EssenceValue)
