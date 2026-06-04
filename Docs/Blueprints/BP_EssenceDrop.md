# BP_EssenceDrop -- Snapshot

**Dernier snapshot :** 04/06/2026  
**Jalon :** SYS-StatSystem pre-audit  
**Path UE5 :** `Content/Systems/Essence/BP_EssenceDrop`  
**Type :** Actor

---

## Variables

| Nom | Type |
|---|---|
| EssenceValue | int64 |
| bCanBePickedUp | bool |

## Composants
- SphereComponent (root, OverlapAllDynamic)
- StaticMesh (NoCollision obligatoire)
- PointLight

---

## Flow ActorBeginOverlap

```
Branch(bCanBePickedUp)
-> Cast HC -> Get AttributeSetRef
-> Get AttributeSetRef.EssenceValue (int64) + self.EssenceValue (int64)
-> To Float (Integer64)           <- conversion 1 : int64 -> double
-> SetStatValue("EssenceValue", double)
  [Dans Switch] Conv_DoubleToInt64 <- conversion 2 : double -> int64
  -> SET AttributeSetRef.EssenceValue (int64)
-> DestroyActor
```

---

## Anomalies

| Anomalie | Description | Impact |
|---|---|---|
| Double conversion int64 <-> double | Pickup : int64 -> double -> SetStatValue -> double -> int64. Perte de precision pour valeurs > 2^53 (~9 quadrillions) | Non critique C1 -- dette architecturale |
| Gotcha StaticMesh | Doit etre en NoCollision sinon bloque overlaps SphereComponent | Comportement valide mais piege classique |
| Gotcha bCanBePickedUp | Delay 1.5s obligatoire -- drop spawne a l'interieur du HC | Comportement valide |

---

*Snapshot produit par audit agent UnrealClaude -- session 04/06/2026*
