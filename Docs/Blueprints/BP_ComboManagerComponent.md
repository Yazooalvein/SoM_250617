# BP_ComboManagerComponent -- Snapshot

**Path UE5 :** `/Game/Systems/Combo/BP_ComboManagerComponent`
**Parent :** ActorComponent
**Noeuds totaux :** 123
**Dernier snapshot :** 05/06/2026 -- Audit global

---

## Variables

| Nom | Type | Notes |
|---|---|---|
| CurrentWeaponID | FName | Source unique arme equipee |
| CurrentWeaponLevel | int32 | |
| CurrentStepID | FName | Etape combo courante |
| CanAttack | bool | Source unique permission attaque |
| bIsInComboWindow | bool | |
| ComboStepMap | TMap<FName,FComboStep> | |
| NextStepID | FName | ⚠️ non utilise -- dette nettoyage |
| AnimToPlay | FName | ⚠️ non utilise -- dette nettoyage |

## Fonctions

| Nom | Inputs | Outputs | Notes |
|---|---|---|---|
| EquipWeapon | WeaponID:FName, WeaponLevel:int32 | -- | SET CurrentWeaponID -- point d'entree unique |
| InitComboTree | WeaponData:FWeaponData | -- | Peuple ComboStepMap depuis DT_Combo |
| HandleAttack | AttackType:EAttackInputType | -- | Logique combo -- lit CurrentWeaponID en interne |
| PlayAttackMontage | StepID:FName | -- | |
| ResetCombo | -- | -- | |
| UpgradeWeaponLevel | NewLevel:int32 | -- | |
| RotateTowardLockTarget | -- | -- | |
| GetOwningMesh | -- | AnimInstance* | |
| GetBP_CombatLockOnComponent | -- | BP_CombatLockOnComponent_C* | |

**EventGraph :** 4 events, 11 noeuds

## Dependances

**Appelle :** BP_CombatLockOnComponent, DT_Combo_Sword
**Appele par :** BP_SoM_HeroCharacter (EquipWeapon), BP_SoM_PlayerController (HandleAttack)
**BPI_Saveable :** oui -- SaveData/LoadData implementes

## Dettes actives

- `NextStepID` et `AnimToPlay` non utilises -> supprimer jalon nettoyage
- LevelMin = 0 dans DT_Combo (regle permanente)

## Notes techniques

- HandleAttack sans parametre ChoosenWeapon -- lit CurrentWeaponID en interne
- Switch arme = reset combo complet (punition Dark Souls style)
- CurrentWeaponID = SOURCE UNIQUE arme equipee -- jamais recreer dans HC
