# BP_AttributeSet_Base -- Snapshot

**Dernier snapshot :** 04/06/2026  
**Jalon :** SYS-StatSystem VALIDE PIE  
**Path UE5 :** `Content/Systems/Stats/BP_AttributeSet_Base`  
**Type :** Actor Component (Parent : Object)  
**Interfaces :** BPI_Saveable (SaveData, LoadData)

---

## Variables

| Nom | Type | Categorie | Notes |
|---|---|---|---|
| StatValues | TMap<Name, double> | Stats | Map principale -- TOUTES les stats sauf EssenceValue |
| StatMinValues | TMap<Name, double> | Stats | Peuple par InitStats depuis DT_StatList.MinValue |
| StatMaxValues | TMap<Name, double> | Stats | Peuple par InitStats depuis DT_StatList.MaxValue |
| HealthMax | double | Stats\|Health | Variable native conservee -- cache synchronise par SetStatValue guard |
| StaminaMax | double | Stats\|Stamina | Variable native conservee -- cache synchronise |
| ManaMax | double | Stats\|Mana | Variable native conservee -- cache synchronise |
| EssenceValue | int64 | Default | Type distinct -- conversion double->int64 dans SetStatValue |
| Corruption | double | Default | Cache synchronise -- clamp selon bCorruptionUnlocked |
| bCorruptionUnlocked | bool | Default | false = plafond 50, true = plafond 100 |
| bIsStaminaRegenerating | bool | Stats\|Stamina | Etat interne timer -- jamais via SetStatValue |
| OnStatChanged | mcdelegate | Default | Dispatcher : StatName(Name) + NewValue(double) |

**Variables natives supprimees (vivaient dans StatValues depuis SYS-StatSystem) :**  
HealthCurrent, StaminaCurrent, StaminaMax (natif supprime -- reste dans StatValues), ManaCurrent, StaminaRegenRate, StaminaCostJump, StaminaCostDash, StaminaRegenDelay, StaminaRegenInterval, TenaciteEtat

---

## Fonctions

| Nom | Inputs | Outputs | Pure | Notes |
|---|---|---|---|---|
| InitStats | StatDataTable:DataTable | -- | Non | GetDataTableRowNames -> ForEach -> GetDataTableRow -> BreakStatStruct -> Map_Add x3 (StatValues, StatMinValues, StatMaxValues) |
| GetStatValue | StatName:Name | double | **Oui** | Map_Find(StatValues, StatName) -> Found: return Value / NotFound: DebugPrint + return 0.0 |
| SetStatValue | StatName:Name, Value:double | -- | Non | 3 guards + Default. 6 CallDelegate OnStatChanged branches. |
| ConsumeStamina | Amount:double | -- | Non | GetStatValue(StaminaCurrent) - Amount -> FClamp(0, GetStatValue(StaminaMax)) -> SetStatValue(StaminaCurrent) -> reset/start regen |
| StartStaminaRegen | -- | -- | Non | Guard: GetStatValue(StaminaCurrent) >= GetStatValue(StaminaMax) -> return. Sinon SET bIsStaminaRegenerating + SetTimer(HandleStaminaRegen) |
| HandleStaminaRegen | -- | -- | Non | GetStatValue(StaminaCurrent) < GetStatValue(StaminaMax) -> SetStatValue(StaminaCurrent, Current + Rate * Interval). Sinon ClearTimer + bIsStaminaRegenerating=false |

**BPI_Saveable :**
- SaveData : GET EssenceValue (int64) -> SET SaveGame.EssenceValue
- LoadData : GET SaveGame.EssenceValue -> To Float -> SetStatValue("EssenceValue"). Puis SetStatValue HP/ST/MP = GetStatValue(Max).

---

## SetStatValue -- detail guards

| Guard | Condition | Logique | Variable native synchronisee |
|---|---|---|---|
| EssenceValue | StatName == "EssenceValue" | Conv_DoubleToInt64(Value) -> SET EssenceValue (int64) -> Map_Add -> CallDelegate | EssenceValue (int64) |
| Corruption | StatName == "Corruption" | Branch(bCorruptionUnlocked): Clamp(0,100) si true / Clamp(0,50) si false -> SET Corruption -> Map_Add -> CallDelegate | Corruption (double) |
| HealthMax | StatName == "HealthMax" | Value -> SET HealthMax natif DIRECTEMENT (sans FMin) -> Map_Add -> CallDelegate | HealthMax (double) |
| Default | Tout le reste | Map_Find(StatMinValues) -> MinValue. Map_Find(StatMaxValues) -> MaxValue. FClamp(Value, Min, Max) -> Map_Add -> CallDelegate | -- |

**GOTCHA critique :** guard HealthMax -- ne jamais utiliser FMin(Value, GetStatValue("HealthCurrent")) comme borne. HealthCurrent peut etre absente de la Map au moment du ForEach InitAttributesFromDatatable -> FMin retourne 0 -> HealthMax = 0.

---

## Appelants de SetStatValue

| Blueprint | Fonction | StatName |
|---|---|---|
| BP_AttributeSet_Base | ConsumeStamina | StaminaCurrent |
| BP_AttributeSet_Base | HandleStaminaRegen | StaminaCurrent |
| BP_AttributeSet_Base | LoadData | EssenceValue, HealthCurrent, StaminaCurrent, ManaCurrent |
| BP_SoM_HeroCharacter | InitAttributesFromDatatable | StatID (dynamique DT), HealthCurrent, StaminaCurrent, ManaCurrent |
| BP_SoM_PlayerController | OnHeroDied | EssenceValue(=0), HealthCurrent, StaminaCurrent, ManaCurrent |
| BP_SoM_GameMode | WriteSaveAndApplyFountainEffects | HealthCurrent, ManaCurrent, StaminaCurrent |
| BP_MagicComponent | ConsumeMana | ManaCurrent |
| BP_CorruptionComponent | TrackDeityUsage | Corruption |
| BP_CorruptionComponent | PurgeCorruption | Corruption(=0) |
| BP_EssenceDrop | ActorBeginOverlap | EssenceValue |
| BP_Spell_Heal | ApplyEffect | HealthCurrent |

---

## OnStatChanged -- bindings

| Blueprint | Role |
|---|---|
| UI_HUD_Main | Seul bindeur -- Bind dans Event Construct -> HUD_OnStatChanged |

---

## DT_StatList -- rows connues

14 rows : HealthMax, StaminaMax, StaminaRegenRate, StaminaRegenInterval, StaminaCostJump, StaminaCostDash, StaminaRegenDelay, ManaMax, TenaciteEtat, EssenceValue, Corruption, (+ autres)  
Pas de rows Current (HealthCurrent, StaminaCurrent, ManaCurrent) -- initialises post-ForEach via SetStatValue(Current = GetStatValue(Max)).

---

*Snapshot mis a jour post-SYS-StatSystem -- 04/06/2026*
