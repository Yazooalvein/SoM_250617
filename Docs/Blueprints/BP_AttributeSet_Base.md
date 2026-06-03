# BP_AttributeSet_Base -- Snapshot

**Dernier snapshot :** 04/06/2026  
**Jalon :** INFRA-BlueprintSnapshotLayer (audit pre-SYS-StatSystem)  
**Path UE5 :** `Content/Systems/Stats/BP_AttributeSet_Base`  
**Type :** Actor Component  
**Interfaces implementees :** BPI_Saveable (SaveData, LoadData)

---

## Variables

| Nom | Type | Categorie | Notes |
|---|---|---|---|
| HealthCurrent | double | Stats\Health | Lue en GET direct par ConsumeStamina, HC EventGraph |
| HealthMax | double | Stats\Health | Lue en GET direct par ConsumeStamina, HC |
| StaminaCurrent | double | Stats\Stamina | Lue en GET direct par ConsumeStamina, StartStaminaRegen, HandleStaminaRegen |
| StaminaMax | double | Stats\Stamina | Lue en GET direct par ConsumeStamina, StartStaminaRegen, HandleStaminaRegen |
| StaminaRegenRate | double | Stats\Stamina | Lue en GET direct par HandleStaminaRegen |
| StaminaCostJump | double | Stats\Stamina | |
| StaminaCostDash | double | Stats\Stamina | |
| StaminaRegenDelay | double | Stats\Stamina | Lue en GET direct par ConsumeStamina |
| StaminaRegenInterval | double | Stats\Stamina | Lue en GET direct par StartStaminaRegen, HandleStaminaRegen |
| bIsStaminaRegenerating | bool | Stats\Stamina | Etat interne timer -- pas une stat modifiable via SetStatValue |
| ManaMax | double | Stats\Mana | |
| ManaCurrent | double | Stats\Mana | |
| EssenceValue | **int64** | Default | TYPE DISTINCT -- conversion double->int64 dans SetStatValue |
| Corruption | double | Default | |
| bCorruptionUnlocked | bool | Default | Flag d'etat -- pas dans DT_StatList -- pilote le clamp Corruption |
| TenaciteEtat | double | Default | Base 25, FClamp(0,100) |
| OnStatChanged | mcdelegate | Default | Dispatcher : StatName (Name) + NewValue (double) |

**Note :** `bIsStaminaRegenerating` et `bCorruptionUnlocked` sont des flags d'etat, pas des stats. Ils ne passent pas par SetStatValue et ne seront pas dans la TMap.

---

## Fonctions

| Nom | Inputs | Outputs | Notes |
|---|---|---|---|
| SetStatValue | StatName: Name, Value: double | -- | Point d'entree unique. Switch 14 cases actuel. A refactoriser -> TMap + DT_StatList |
| ConsumeStamina | Amount: double | -- | Calcule StaminaCurrent - Amount, clamp(0, StaminaMax), appelle SetStatValue("StaminaCurrent"). Puis ClearTimer + SET bIsStaminaRegenerating + SetTimer(StartStaminaRegen, StaminaRegenDelay) |
| StartStaminaRegen | -- | -- | Guard : si StaminaCurrent >= StaminaMax -> return. Sinon SET bIsStaminaRegenerating=true + SetTimer(HandleStaminaRegen, StaminaRegenInterval, looping=true) |
| HandleStaminaRegen | -- | -- | Si StaminaCurrent < StaminaMax : SetStatValue("StaminaCurrent", Current + Rate*Interval). Sinon : ClearTimer + SET bIsStaminaRegenerating=false |
| SaveData (BPI_Saveable) | SaveGame ref | -- | Ecrit EssenceValue dans SaveGame |
| LoadData (BPI_Saveable) | SaveGame ref | -- | Lit EssenceValue depuis SaveGame. HP/ST/MP remis a Max via SetStatValue |

---

## Appelants externes de SetStatValue

| Blueprint | Fonction appelante | StatName | Valeur |
|---|---|---|---|
| BP_SoM_HeroCharacter | EventGraph | HealthCurrent | damage calcule |
| BP_SoM_HeroCharacter | InitAttributesFromDatatable | depuis DataTable row (dynamique) | BaseValue |
| BP_SoM_HeroCharacter | InitAttributesFromDatatable | HealthCurrent, StaminaCurrent, ManaCurrent | valeurs initiales |
| BP_SoM_PlayerController | EventGraph (OnHeroDied) | EssenceValue | 0 (hardcode) |
| BP_SoM_PlayerController | EventGraph (OnHeroDied) | HealthCurrent, StaminaCurrent, ManaCurrent | Max |
| BP_SoM_GameMode | WriteSaveAndApplyFountainEffects | HealthCurrent, ManaCurrent | Max |
| BP_MagicComponent | ConsumeMana | ManaCurrent | Current - cost |
| BP_CorruptionComponent | TrackDeityUsage | Corruption | Current + 5.0 |
| BP_CorruptionComponent | PurgeCorruption | Corruption | 0 (hardcode) |
| BP_EssenceDrop | EventGraph (ActorBeginOverlap) | EssenceValue | valeur du drop |
| BP_AttributeSet_Base | LoadData (BPI_Saveable) | EssenceValue | valeur sauvegardee |
| BP_Spell_Heal | ApplyEffect | HealthCurrent | soin calcule |
| BP_Spell_Buff | EventGraph | depuis parametre/data (dynamique) | variable |
| BP_Spell_Buff | ApplyEffect | depuis parametre/data (dynamique) | variable |

**BPs sans appel SetStatValue :** BP_Spell_Attack, BP_Spell_Debuff, BP_ComboManagerComponent, BP_InventoryComponent, BP_Enemy_Base, BP_Enemy_TestBed, UI_HUD_Main.

---

## Lecteurs de stats (acces direct aux variables natives)

| Blueprint | Fonction | Variable lue | Usage |
|---|---|---|---|
| BP_SoM_HeroCharacter | EventGraph | HealthCurrent | logique mort/respawn |
| BP_SoM_HeroCharacter | InitAttributesFromDatatable | HealthMax | calcul HealthCurrent initial |
| BP_AttributeSet_Base | SaveData (BPI_Saveable) | EssenceValue | ecriture SaveGame |
| UI_HUD_Main | EventGraph | via OnStatChanged dispatcher | reception StatName + NewValue |
| UI_HUD_Main | UpdateStatText / InitHUD | via OnStatChanged (appele 2x) | initialisation HUD |

**Note :** `GetStatValue` n'existe pas encore. Tous les lecteurs externes passent par GET direct sur les variables natives, ou via le dispatcher OnStatChanged.

---

## OnStatChanged -- bindings

| Blueprint | Role | Notes |
|---|---|---|
| BP_AttributeSet_Base | Definition + appel | Call OnStatChanged en fin de chaque case du Switch (15 connexions exec entrantes) |
| UI_HUD_Main | Seul bindeur | Bind Event to OnStatChanged -> HUD_OnStatChanged (Custom Event) dans EventGraph |

HC et PC ne bindent pas directement. Le binding est initialise depuis HC.Add_Main_HUD qui passe l'AttributeSetRef au widget.

---

## Bugs actifs (confirmes par audit T3D)

| Bug | Description | Impact | Jalon cible |
|---|---|---|---|
| ErrorType=1 x8 | HealthMax, StaminaMax, ManaMax, StaminaCostJump, StaminaRegenRate, StaminaRegenDelay, StaminaRegenInterval, StaminaCurrent (dans ConsumeStamina/StartStaminaRegen) -- GUIDs variables obsoletes apres migration | Nodes rouges en editeur, comportement impredictible | SYS-StatSystem |
| Bug HealthMax guard | FMin node present (Value, HealthCurrent) mais pin B non connecte -- clamp vers 0 au lieu de HealthCurrent | HealthMax peut depasser HealthCurrent | SYS-StatSystem |

---

## Assets lies non branches (dette d'architecture)

| Asset | Path | Statut |
|---|---|---|
| DT_StatList | Content/Systems/Stats/ | Existe, 11 rows, NON branche sur BP_AttributeSet_Base |
| StatStruct | Content/Systems/Stats/ | Existe (StatID, DisplayName, Description, Type, Element, BaseValue, MinValue, MaxValue, IsModifiable, Icone, GameplayTag) |
| EStatType | Content/Systems/Stats/ | Existe (Principal, Elem, Second, Progression, Temp) |
| EElementType | Content/Systems/Stats/ | Existe (None, Athanor, Dryade, Gnome, Lumina, Luna, Ombre, Ondine, Sylphide) |

---

## Plan SYS-StatSystem (architecture cible)

```
BeginPlay -> InitStats()
  GetDataTableRowNames(DT_StatList) -> ForEach
    GetDataTableRow(DT_StatList, RowName) -> StatStruct
    MAP SET StatValues[StatStruct.StatID] = StatStruct.BaseValue
    SET variable native = StatStruct.BaseValue  (cache synchronise)

SetStatValue(StatName, Value)
  GetDataTableRow(DT_StatList, StatName) -> StatStruct (pour Min/Max)
  [Guard EssenceValue] -> Conv_DoubleToInt64 -> SET EssenceValue (native)
  [Guard Corruption]   -> bCorruptionUnlocked ? FClamp(0,100) : FClamp(0,50)
  [Guard HealthMax]    -> FMin(Value, GET StatValues["HealthCurrent"])  <- bug fixe
  [Default]            -> FClamp(Value, StatStruct.MinValue, StatStruct.MaxValue)
  MAP SET StatValues[StatName] = ClampedValue
  SET variable native = ClampedValue  (cache synchronise pour lecteurs internes)
  Broadcast OnStatChanged(StatName, ClampedValue)

GetStatValue(StatName) -> double  [Pure]
  MAP FIND StatValues[StatName]
    Found    -> Return Value
    NotFound -> PrintString(Warning) + Return 0.0
```

**Variables natives conservees :** cache synchronise pour ConsumeStamina, HandleStaminaRegen, StartStaminaRegen qui lisent en GET direct. Pas de migration de ces fonctions dans SYS-StatSystem.

---

*Snapshot produit par audit agent UnrealClaude + analyse T3D -- session 04/06/2026*
