# BP_CorruptionComponent -- Snapshot

**Dernier snapshot :** 04/06/2026  
**Jalon :** SYS-StatSystem pre-audit  
**Path UE5 :** `Content/Systems/Corruption/BP_CorruptionComponent`  
**Type :** Actor Component

---

## Variables

| Nom | Type | Statut |
|---|---|---|
| DeityUsageMap | TMap<Name, int32> | OK |
| **OwnerAttributeSet** | BP_AttributeSet_Base_C* | **DETTE** -- stockage interdit par CLAUDE.md |

---

## Fonctions

| Nom | SetStatValue | Flow |
|---|---|---|
| InitCorruption | Aucun | Re-fetch AttributeSet via GetOwner->Cast->GET AttributeSetRef -> SET OwnerAttributeSet |
| TrackDeityUsage(DeityName) | "Corruption" | Re-fetch AttributeSetRef -> SET OwnerAttributeSet -> GET Corruption -> +5.0 -> Clamp(0,100) pre-SetStatValue -> SetStatValue("Corruption", clamped) |
| PurgeCorruption(CostAmount) | "Corruption" | Re-fetch -> SetStatValue("Corruption", 0.0) + Map_Clear(DeityUsageMap) |
| GetWeakDeity | Aucun | Retourne la deite la plus utilisee depuis la derniere purge |

---

## Anomalies

| Anomalie | Description | Impact |
|---|---|---|
| OwnerAttributeSet stocke en variable | Contradite par CLAUDE.md (ne pas stocker AttributeSetRef) | Attenué : re-fetch systématique avant chaque usage. Reste une dette. |
| Clamp redondant dans TrackDeityUsage | Pre-clamp a (0,100) avant SetStatValue IGNORE la logique Phase1/Phase2 (bCorruptionUnlocked). Le bon clamp est dans SetStatValue.Switch uniquement. | Corruption peut atteindre 100 en Phase 1 via ce chemin |

**Clamp redondant -- detail :**
TrackDeityUsage fait `Clamp(Corruption+5, 0, 100)` avant SetStatValue. Mais SetStatValue re-clamp selon `bCorruptionUnlocked` (0-50 ou 0-100). Le pre-clamp est donc au mieux redondant, au pire incorrect en Phase 1 (il laisse passer des valeurs > 50 que SetStatValue corrige ensuite). A supprimer dans SYS-StatSystem.

---

*Snapshot produit par audit agent UnrealClaude -- session 04/06/2026*
