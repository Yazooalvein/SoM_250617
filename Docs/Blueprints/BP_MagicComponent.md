# BP_MagicComponent -- Snapshot

**Dernier snapshot :** 04/06/2026  
**Jalon :** SYS-StatSystem pre-audit  
**Path UE5 :** `Content/Systems/Magic/Core/BP_MagicComponent`  
**Type :** Actor Component  
**Interfaces :** BPI_Saveable

---

## Variables

| Nom | Type |
|---|---|
| bIsCasting | bool |
| QuickslotSlots | Array<Name> |
| SpellCooldowns | TMap<Name, double> |
| UnlockedSpells | TMap<Name, FSoM_DeitySpells> |
| OnSpellCast | mcdelegate (SpellID:Name) |
| SpellUsageCounts | TMap<Name, int32> |
| SpellLevels | TMap<Name, int32> |
| TalentPoints | int32 |
| LockedDeities | Array<Name> |
| CategoryThresholdsConfig | BP_SpellCategoryThresholds_C* |

---

## Fonctions

| Nom | SetStatValue | Notes |
|---|---|---|
| CastSpell | Aucun direct | Appelle ConsumeMana (indirect) + IncrementSpellUsage (indirect) |
| ConsumeMana | "ManaCurrent" | GetOwner -> Cast HC -> Get AttributeSetRef -> Get ManaCurrent -> subtract Amount -> SetStatValue |
| IncrementSpellUsage | Aucun direct | GetComponentByClass -> TrackDeityUsage (indirect, SetStatValue("Corruption") dans CorruptionComponent) |
| UnlockDeity | Aucun | Lit DT_Deities |
| LockDeity | Aucun | |
| IsDeityAccessible | Aucun | Contains(UnlockedSpells) AND NOT Contains(LockedDeities) |
| LevelUpSpell | Aucun | |
| SaveData (BPI_Saveable) | Aucun | |
| LoadData (BPI_Saveable) | Aucun | SetStatValue pas utilise -- reconstruction via UnlockDeity |

---

## Anomalies

| Anomalie | Description |
|---|---|
| Cast orphelin dans IncrementSpellUsage | K2Node_CastTo BP_CorruptionComponent (pos_x=4320) avec 0 connexions exec -- noeud mort a nettoyer |
| Acces AttributeSet indirect | ConsumeMana : GetOwner -> Cast HC -> AttributeSetRef -> ManaCurrent. Pattern correct mais verbeux -- apres SYS-StatSystem, GetStatValue("ManaCurrent") sera disponible |

---

*Snapshot produit par audit agent UnrealClaude -- session 04/06/2026*
