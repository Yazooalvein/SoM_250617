# BP_CorruptionComponent -- Snapshot

**Path UE5 :** `/Game/Systems/Corruption/BP_CorruptionComponent`
**Parent :** ActorComponent
**Noeuds totaux :** 53
**Dernier snapshot :** 05/06/2026 -- Audit global

---

## Variables

| Nom | Type | Notes |
|---|---|---|
| DeityUsageMap | TMap<FName,int32> | Usages par deite depuis derniere purge |

## Fonctions

| Nom | Inputs | Outputs | Notes |
|---|---|---|---|
| InitCorruption | -- | -- | |
| TrackDeityUsage | DeityName:FName | -- | Incremente Map + Corruption +5 via SetStatValue |
| GetWeakDeity | -- | FName | Deite la plus utilisee depuis derniere purge |
| PurgeCorruption | CostAmount:double | -- | SetStatValue(Corruption,0) + Map_Clear(DeityUsageMap) |

## Dependances

**Appelle :** BP_AttributeSet_Base (SetStatValue -- recup dynamique GetOwner->Cast, jamais variable stockee)
**Appele par :** BP_MagicComponent (TrackDeityUsage apres CastSpell), BP_SoM_GameMode (PurgeCorruption via Se reposer fontaine)

## Notes techniques

- NE PAS stocker AttributeSetRef en variable -- recup dynamiquement GetOwner->Cast a chaque appel
- Corruption faiblesse 75 = deite la plus utilisee DEPUIS LA DERNIERE PURGE (pas depuis debut partie)
- Phase 1 plafond 50 (bCorruptionUnlocked=false) / Phase 2 plafond 100 (bCorruptionUnlocked=true)
- +5 Corruption par sort = POC C1 -- calibrage SESSION-Economie
