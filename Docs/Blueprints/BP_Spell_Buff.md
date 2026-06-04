# BP_Spell_Buff -- Snapshot

**Dernier snapshot :** 04/06/2026  
**Jalon :** SYS-StatSystem pre-audit  
**Path UE5 :** `Content/Systems/Magic/Spells/Lumina/BP_Spell_Buff`  
**Type :** Actor (Parent : BP_Spell_Base)

---

## Variables

| Nom | Type | Notes |
|---|---|---|
| OriginalHealthMax | double | Sauvegarde de HealthMax avant application du buff |

---

## SetStatValue -- 2 appels, StatName DYNAMIQUE

| Emplacement | StatName | Valeur | Dynamique |
|---|---|---|---|
| ApplyEffect | SpellData.AffectedStat_36 | HealthMax + EffectValues | **OUI** |
| RestoreStats (Custom Event) | SpellData.AffectedStat_36 | OriginalHealthMax | **OUI** |

**Flow ApplyEffect :**
```
Guard : OriginalHealthMax <= 0 (first application seulement)
SET OriginalHealthMax = GET AttributeSetRef.HealthMax
SetStatValue(AffectedStat, HealthMax + EffectValues)
Set Timer -> RestoreStats (duree = SpellData.Duration)
```

**Flow RestoreStats :**
```
Cast HC -> Get AttributeSetRef
Break SpellData -> AffectedStat_36
SetStatValue(AffectedStat, OriginalHealthMax)
SET OriginalHealthMax = 0
DestroyActor
```

**Implication pour SYS-StatSystem :** L'API SetStatValue(Name, double) doit rester inchangee. Le StatName dynamique depuis SpellData.AffectedStat fonctionne avec la TMap exactement comme avec le Switch (MAP FIND sur une cle Name).

---

*Snapshot produit par audit agent UnrealClaude -- session 04/06/2026*
