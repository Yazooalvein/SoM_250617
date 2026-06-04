# BP_AttributeSet_Base -- Snapshot

**Path UE5 :** `/Game/Systems/Stats/BP_AttributeSet_Base`
**Parent :** Object
**Noeuds totaux :** 100
**Dernier snapshot :** 05/06/2026 -- Audit global

---

## Variables

| Nom | Type | Categorie | Notes |
|---|---|---|---|
| StatValues | TMap<FName,double> | Stats | Stocke Current de toutes les stats |
| StatMinValues | TMap<FName,double> | Stats | |
| StatMaxValues | TMap<FName,double> | Stats | |
| HealthMax | double | Stats\|Health | Natif -- synchronise par guard SetStatValue |
| StaminaMax | double | Stats\|Stamina | Natif |
| ManaMax | double | Stats\|Mana | Natif |
| StaminaCurrent | double | Stats\|Stamina | ⚠️ variable native residuelle -- Current doit vivre UNIQUEMENT dans StatValues |
| StaminaRegenRate | double | Stats\|Stamina | |
| StaminaCostJump / StaminaCostDash | double | Stats\|Stamina | |
| StaminaRegenDelay / StaminaRegenInterval | double | Stats\|Stamina | |
| bIsStaminaRegenerating | bool | Stats\|Stamina | |
| OnStatChanged | Dispatcher | Default | Notifie le HUD |
| EssenceValue | int64 | Default | ⚠️ doublon -- aussi dans StatValues -- a unifier C2 |
| Corruption | double | Default | ⚠️ doublon -- aussi dans StatValues -- a unifier C2 |
| bCorruptionUnlocked | bool | Default | Phase 1 plafond 50 / Phase 2 plafond 100 |
| TenaciteEtat | double | Default | Base 25, dans StatValues |

## Fonctions

| Nom | Inputs | Outputs | Notes |
|---|---|---|---|
| GetStatValue | StatName:FName | double (Pure) | Lecteur universel -- Map_Find + debug si absent |
| SetStatValue | StatName:FName, Value:double | -- | Guards EssenceValue + Corruption + HealthMax + Default (FClamp) + 6x CallDelegate |
| InitStats | StatDataTable:DataTable* | -- | ForEach DT_StatList -> Map_Add x3 |
| ConsumeStamina | Amount:double | -- | Via GetStatValue + SetStatValue |
| StartStaminaRegen | -- | -- | Lance timer regen |
| HandleStaminaRegen | -- | -- | Callback timer |

**EventGraph :** 2 events, 7 noeuds

## Dependances

**Appelle :** DT_StatList
**Appele par :** BP_SoM_HeroCharacter (AttributeSetRef), UI_HUD_Main (InitHUD), BP_MagicComponent (ConsumeMana), BP_CorruptionComponent (TrackDeityUsage, PurgeCorruption)

## Dettes actives

- `StaminaCurrent` variable native residuelle -> supprimer C2, Current uniquement dans StatValues
- `EssenceValue` et `Corruption` dupliques native + StatValues -> unifier C2

## Notes techniques critiques

- Variables natives : HealthMax, StaminaMax, ManaMax UNIQUEMENT
- HealthCurrent/StaminaCurrent/ManaCurrent : StatValues UNIQUEMENT -- pas de native
- Guard HealthMax : Value -> SET HealthMax natif DIRECTEMENT -- jamais FMin(Value, GetStatValue(HealthCurrent))
- GOTCHA : FMin(Value, GetStatValue(HealthCurrent)) dans guard HealthMax -> HealthMax=0 si HealthCurrent absente au ForEach
- SetStatValue = UNIQUE point de modification stats -- zero exception
- GetStatValue(Name) = UNIQUE point de lecture stats
