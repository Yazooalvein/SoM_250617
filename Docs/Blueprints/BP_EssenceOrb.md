# BP_EssenceOrb -- Snapshot

**Path UE5 :** `/Game/Systems/Essence/BP_EssenceOrb`
**Parent :** Actor
**Dernier snapshot :** 06/06/2026 -- ENEMY-DropSystem

---

## Role

Drop actif DS-like spawne a la mort d'un ennemi. Vole automatiquement vers le hero et credite l'Essence a l'arrivee.
Distinct de BP_EssenceDrop (passif, mort hero).

## Composants

- SphereComponent (root)
- StaticMeshComponent (NoCollision obligatoire)
- PointLight

## Variables

| Nom | Type | Notes |
|---|---|---|
| EssenceDropValue | int64 | Valeur Essence a crediter. SET depuis BP_Enemy_Base apres spawn. |
| TargetCharacter | BP_SoM_HeroCharacter | Ref HC, SET en BeginPlay via GetPlayerCharacter |
| FlySpeed | float | Vitesse VInterpTo (default a tuner en Details panel) |
| ArrivalThreshold | float | Distance seuil declenchant OnArrival (default a tuner) |

## EventGraph

- **BeginPlay :** GetPlayerCharacter -> Cast HC -> SET TargetCharacter
- **Tick :** IsValid(TargetCharacter) -> VInterpTo(Self, Target, DeltaSeconds, FlySpeed) -> SetActorLocation. VSize(Target-Self) < ArrivalThreshold -> OnArrival

## Fonctions

| Nom | Notes |
|---|---|
| OnArrival | GetStatValue(EssenceValue) + EssenceDropValue -> Conv_Int64ToDouble -> SetStatValue(EssenceValue) -> DestroyActor |

## Dependances

**Appelle :** BP_AttributeSet_Base (GetStatValue + SetStatValue)
**Spawn par :** BP_Enemy_Base (OnDeath)

## Dettes actives

- EssenceDropValue hardcode depuis BP_Enemy_Base (15 en C1) -> DT_Enemy C2
- DebugPrintVar a supprimer avant MAP-C1Level

## Notes techniques

- VInterpTo OBLIGATOIRE (pas VLerp -- alpha = DeltaSeconds * FlySpeed > 1 depasse la cible)
- Condition arrivee : VSize < ArrivalThreshold (pas >) -- bug classique a ne pas reproduire
- StaticMesh NoCollision obligatoire
