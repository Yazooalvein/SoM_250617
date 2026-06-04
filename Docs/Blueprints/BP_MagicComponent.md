# BP_MagicComponent -- Snapshot

**Path UE5 :** `/Game/Systems/Magic/Core/BP_MagicComponent`
**Parent :** ActorComponent
**Noeuds totaux :** 187
**Dernier snapshot :** 05/06/2026 -- Audit global

---

## Variables

| Nom | Type | Notes |
|---|---|---|
| bIsCasting | bool | |
| QuickslotSlots | TArray<FName> | Sorts assignes slots rapides |
| UnlockedSpells | TMap<FName,FSoM_DeitySpells> | Sorts accessibles |
| LockedDeities | TArray<FName> | Deites verrouillees -- sauvegarde (delta) |
| SpellCooldowns | TMap<FName,double> | |
| SpellUsageCounts | TMap<FName,int32> | |
| SpellLevels | TMap<FName,int32> | |
| TalentPoints | int32 | |
| OnSpellCast | Dispatcher | |
| CategoryThresholdsConfig | BP_SpellCategoryThresholds_C* | |

## Fonctions

| Nom | Inputs | Outputs | Notes |
|---|---|---|---|
| CastSpell | SpellID:FName | -- | Point d'entree unique lancement sort |
| CanCast | SpellID:FName | bool | |
| ConsumeMana | Amount:double | -- | Via GetStatValue + SetStatValue |
| IsDeityAccessible | DeityID:FName | bool | Contains(UnlockedSpells) AND NOT Contains(LockedDeities) |
| IsSpellUnlocked | SpellID:FName | bool | |
| UnlockDeity | DeityName:FName | -- | "Set Members in FSoM_DeitySpells" -- PAS Make |
| LockDeity | DeityID:FName | -- | |
| IncrementSpellUsage | SpellID:FName | -- | |
| LevelUpSpell | SpellID:FName | -- | |
| AddTalentPoint | -- | -- | |

## Dependances

**Appelle :** BP_AttributeSet_Base (ConsumeMana via GetStatValue/SetStatValue), DT_Deities, DT_Spells, BP_Spell_Base sous-classes
**Appele par :** BP_SoM_PlayerController (CastSpell quickslot), UI_Radial_Main (ValidateRadial)
**BPI_Saveable :** oui -- LockedDeities sauvegarde, UnlockedSpells reconstruit depuis DT_Deities au load

## Notes techniques

- UnlockDeity : "Set Members in FSoM_DeitySpells" NON "Make FSoM_DeitySpells" -- Make a bDefaultValueIsIgnored=True
- UnlockDeity Map_Contains : TRUE = deja present -> return (guard)
- IsDeityAccessible = Contains(UnlockedSpells) AND NOT Contains(LockedDeities)
- DT_Deities BaseSpells : [0=Attack, 1=Heal, 2=Buff, 3=Debuff]
- Deite C1 : Lumina uniquement
- Sauvegarde : LockedDeities (delta) -- UnlockedSpells reconstruit depuis DT_Deities au load
