# UI_Radial_Main -- Snapshot

**Path UE5 :** `/Game/UI/Widgets/RadialMenu/UI_Radial_Main`
**Parent :** UserWidget
**Noeuds totaux :** 234
**Dernier snapshot :** 05/06/2026 -- Audit global

---

## Variables

| Nom | Type | Notes |
|---|---|---|
| CurrentCategory | ERadialMode | Mode actuel (Weapons/Magic/etc.) |
| SelectedIndex | int32 | Slot selectionne |
| SlotWidgets | TArray<UI_RadialSlot_C*> | |
| SlotDataList | TArray<FSoM_RadialSlotData> | |
| RadialRadius | double | |
| TargetRotation / CurrentRotation / RotationSpeed / InterpSpeed | double | Animation rotation |
| CurrentMagicSchool | FName | Ecole active |
| MagicComponentRef | BP_MagicComponent_C* | |

## Fonctions

| Nom | Notes |
|---|---|
| GenerateSlots | Cree les UI_RadialSlot |
| UpdateCenterInfo | |
| UpdateSelection(AxisValue:double) | Navigation stick |
| PopulateWeaponSlots | Lit InventoryComponent.GetWeapons() |
| SwitchCategory(Direction:int32) | Change Weapons/Magic |
| ValidateSelectedWeapon | |
| PopulateMagicSchools | Lit DT_Deities |
| PopulateMagicSpells(SchoolID:FName) | Lit DT_Spells |

## Dependances

**Appelle :** BP_InventoryComponent.GetWeapons(), BP_MagicComponent, DT_Deities, DT_Spells
**Gere par :** BP_SoM_PlayerController (OpenRadial, CloseRadial, ValidateRadial)

## Notes techniques

- ERadialMode : 3 valeurs -- Weapons / Deity / Spell
- RadialContainer size = 0.01x0.01 pour pivot quasi-point (fix drift rotation)
- Time Dilation 0.2 (slow-mo radial)
- Radial curseur position initiale incorrecte a l'ouverture -> UI-RadialRefacto C2
