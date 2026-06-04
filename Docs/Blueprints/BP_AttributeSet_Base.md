# BP_AttributeSet_Base -- Snapshot

**Dernier snapshot :** 04/06/2026  
**Jalon :** SYS-StatSystem pre-audit (audit agent complet)  
**Path UE5 :** `Content/Systems/Stats/BP_AttributeSet_Base`  
**Type :** Actor Component (Parent : Object)  
**Interfaces :** BPI_Saveable (SaveData, LoadData)

---

## Variables (17)

| Nom | Type | Categorie | Notes |
|---|---|---|---|
| HealthCurrent | double | Stats\|Health | Lue en GET direct par ConsumeStamina, HC EventGraph |
| HealthMax | double | Stats\|Health | Lue en GET direct par HC InitAttributesFromDatatable, UI_HUD_Main |
| StaminaCurrent | double | Stats\|Stamina | Lue en GET direct par ConsumeStamina, StartStaminaRegen, HandleStaminaRegen |
| StaminaMax | double | Stats\|Stamina | Lue en GET direct par ConsumeStamina, StartStaminaRegen, HandleStaminaRegen, UI_HUD_Main |
| StaminaRegenRate | double | Stats\|Stamina | Lue en GET direct par HandleStaminaRegen |
| StaminaCostJump | double | Stats\|Stamina | |
| StaminaCostDash | double | Stats\|Stamina | |
| StaminaRegenDelay | double | Stats\|Stamina | Lue en GET direct par ConsumeStamina |
| StaminaRegenInterval | double | Stats\|Stamina | Lue en GET direct par StartStaminaRegen, HandleStaminaRegen |
| bIsStaminaRegenerating | bool | Stats\|Stamina | Etat interne timer -- jamais passe par SetStatValue |
| ManaMax | double | Stats\|Mana | Lue en GET direct par UI_HUD_Main, BP_SoM_GameMode |
| ManaCurrent | double | Stats\|Mana | Lue en GET direct par BP_MagicComponent.ConsumeMana |
| EssenceValue | **int64** | Default | TYPE DISTINCT -- conversion double->int64 dans SetStatValue |
| Corruption | double | Default | |
| bCorruptionUnlocked | bool | Default | Flag etat -- pilote clamp Corruption -- pas dans DT_StatList |
| TenaciteEtat | double | Default | Base 25, FClamp(0,100) |
| OnStatChanged | mcdelegate | Default | Dispatcher : StatName(Name) + NewValue(double) |

---

## Fonctions (4)

| Nom | Inputs | Description |
|---|---|---|
| SetStatValue | StatName:Name, Value:double | Switch 14 cases -> SET variable native -> Call OnStatChanged |
| ConsumeStamina | Amount:double | StaminaCurrent-Amount -> Clamp(0,StaminaMax) -> SetStatValue("StaminaCurrent") -> reset/start regen timer |
| StartStaminaRegen | -- | Guard si StaminaCurrent >= StaminaMax -> return. Sinon SET bIsStaminaRegenerating=true + SetTimer(HandleStaminaRegen, looping) |
| HandleStaminaRegen | -- | Si StaminaCurrent < StaminaMax : SetStatValue("StaminaCurrent", Current+Rate*Interval). Sinon : ClearTimer + SET bIsStaminaRegenerating=false |

**BPI_Saveable :**
- SaveData : GET self.EssenceValue (int64) -> SET SaveGame.EssenceValue
- LoadData : GET SaveGame.EssenceValue (int64) -> To Float -> SetStatValue("EssenceValue", float). Puis SetStatValue HP/ST/MP = Max.

---

## SetStatValue -- Switch 14 cases

| Case | Logique speciale | Statut |
|---|---|---|
| HealthCurrent | SET direct | OK |
| HealthMax | Min(Value, HealthCurrent) node present MAIS pin B non connecte -> clamp vers 0 | **BUG ACTIF** |
| StaminaCurrent | SET direct | OK |
| StaminaMax | SET direct | OK |
| ManaCurrent | SET direct | OK |
| ManaMax | SET direct | OK |
| StaminaCostJump | SET direct | OK |
| StaminaCostDash | SET direct | OK |
| StaminaRegenRate | SET direct | OK |
| StaminaRegenDelay | SET direct | OK |
| StaminaRegenInterval | SET direct | OK |
| Corruption | Branch(bCorruptionUnlocked) -> Clamp(0,100) si true / Clamp(0,50) si false -> 2 SET nodes | OK (logique correcte) |
| TenaciteEtat | FClamp(0,100) -> SET | OK |
| EssenceValue | Conv_DoubleToInt64(Value) -> SET (int64) | OK |

**Call OnStatChanged :** 15 connexions exec entrantes. NewValue = parametre double d'entree (pour EssenceValue, NewValue reste double pre-conversion).

---

## Appelants externes de SetStatValue (inventaire complet)

| Blueprint | Fonction | StatName | Dynamique |
|---|---|---|---|
| BP_AttributeSet_Base | ConsumeStamina | StaminaCurrent | Non |
| BP_AttributeSet_Base | LoadData (BPI_Saveable) | EssenceValue | Non |
| BP_SoM_HeroCharacter | InitAttributesFromDatatable | StatID depuis DT_StatList | **OUI** |
| BP_SoM_HeroCharacter | InitAttributesFromDatatable | HealthCurrent, StaminaCurrent, ManaCurrent | Non |
| BP_SoM_PlayerController | OnHeroDied | EssenceValue (=0 hardcode) | Non |
| BP_SoM_PlayerController | OnHeroDied | HealthCurrent, StaminaCurrent, ManaCurrent | Non |
| BP_SoM_GameMode | WriteSaveAndApplyFountainEffects | HealthCurrent, ManaCurrent | Non |
| BP_MagicComponent | ConsumeMana | ManaCurrent | Non |
| BP_CorruptionComponent | TrackDeityUsage | Corruption | Non |
| BP_CorruptionComponent | PurgeCorruption | Corruption (=0 hardcode) | Non |
| BP_EssenceDrop | ActorBeginOverlap | EssenceValue | Non |
| BP_Spell_Heal | ApplyEffect | HealthCurrent | Non |
| BP_Spell_Buff | ApplyEffect | SpellData.AffectedStat | **OUI** |
| BP_Spell_Buff | RestoreStats | SpellData.AffectedStat | **OUI** |

**BPs sans appel :** BP_Spell_Attack, BP_Spell_Debuff, BP_ComboManagerComponent, BP_InventoryComponent, BP_Enemy_Base, BP_Enemy_TestBed.

---

## OnStatChanged -- bindings

| Blueprint | Role |
|---|---|
| BP_AttributeSet_Base | Definition + Call (15 connexions exec entrantes) |
| UI_HUD_Main | Seul bindeur -- Bind dans Event Construct -> HUD_OnStatChanged(StatName, NewValue) |

---

## Bugs actifs confirmes

| Bug | Description | Impact | Fix cible |
|---|---|---|---|
| Guard HealthMax mort | FMin node present, pin B non connecte -> clamp vers 0 | HealthMax peut depasser HealthCurrent | SYS-StatSystem |
| ErrorType=1 x8 | HealthMax, StaminaMax, ManaMax, StaminaCostJump, StaminaRegenRate, StaminaRegenDelay, StaminaRegenInterval, StaminaCurrent (dans ConsumeStamina/StartStaminaRegen) | Nodes rouges, comportement impredictible | SYS-StatSystem |

---

## Assets lies (non branches)

| Asset | Path | Statut |
|---|---|---|
| DT_StatList | Content/Systems/Stats/ | Existe, 11 rows, NON branche |
| StatStruct | Content/Systems/Stats/ | Existe, champs confirmes |
| EStatType | Content/Systems/Stats/ | Existe (Principal, Elem, Second, Progression, Temp) |
| EElementType | Content/Systems/Stats/ | Existe (None + 8 deites) |

---

## Architecture cible SYS-StatSystem

```
BeginPlay -> InitStats()
  GetDataTableRowNames(DT_StatList) -> ForEach
    GetDataTableRow -> BreakStatStruct
    MAP SET StatValues[StatID] = BaseValue
    SET variable native = BaseValue  (cache synchronise)

SetStatValue(StatName, Value : double)
  GetDataTableRow(DT_StatList, StatName) -> MinValue, MaxValue
  [Guard EssenceValue]  -> Conv_DoubleToInt64 -> SET native. Return.
  [Guard Corruption]    -> Branch(bCorruptionUnlocked) -> Clamp(0,100) ou Clamp(0,50)
  [Guard HealthMax]     -> FMin(Value, GET StatValues["HealthCurrent"])  <- bug fixe
  [Default]             -> FClamp(Value, MinValue, MaxValue)
  MAP SET StatValues[StatName] = ClampedValue
  SET variable native = ClampedValue
  Broadcast OnStatChanged(StatName, ClampedValue)

GetStatValue(StatName : Name) -> double  [Pure]
  MAP FIND StatValues[StatName]
    Found    -> Return Value
    NotFound -> PrintString(Warning) + Return 0.0
```

**Variables natives conservees comme cache synchronise** pour ConsumeStamina, HandleStaminaRegen, StartStaminaRegen et UI_HUD_Main qui lisent en GET direct.

---

*Snapshot produit par audit agent UnrealClaude -- session 04/06/2026*
