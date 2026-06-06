# BP_EssenceDrop -- Snapshot

**Path UE5 :** `/Game/Systems/Essence/BP_EssenceDrop`
**Parent :** Actor
**Dernier snapshot :** 06/06/2026 -- ENEMY-DropSystem

---

## Role

Drop passif au sol spawne a la mort du HERO. Le joueur doit se deplacer pour le recuperer.
Distinct de BP_EssenceOrb (actif, mort ennemi).

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
**Spawn par :** BP_SoM_PlayerController (OnHeroDied)

## Notes techniques

- StaticMesh NoCollision OBLIGATOIRE (sinon bloque le joueur)
- bCanBePickedUp + Delay 1.5s OBLIGATOIRE (sinon pickup immediat avant que le drop soit visible)
- EssenceValue configurable a la creation (SpawnActor -> SET EssenceValue)
- MORT HERO UNIQUEMENT -- ne pas utiliser pour les drops ennemis (utiliser BP_EssenceOrb)
