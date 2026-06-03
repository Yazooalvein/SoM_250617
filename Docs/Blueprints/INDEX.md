# Blueprint Snapshot Index -- Shadow of Mana

Ce fichier liste tous les Blueprints documentes avec leur date de dernier snapshot.
Un snapshot perime (> 1 jalon sans mise a jour) = audit agent requis avant modification.

---

## Regle de lecture

Avant tout travail sur un BP, Claude lit le fichier snapshot correspondant.
Si absent ou marque PERIME : lancer un audit UnrealClaude avant de continuer.

---

## Blueprints documentes

| Blueprint | Fichier | Dernier snapshot | Jalon | Statut |
|---|---|---|---|---|
| BP_AttributeSet_Base | [BP_AttributeSet_Base.md](BP_AttributeSet_Base.md) | 04/06/2026 | INFRA-BlueprintSnapshotLayer | A JOUR |

---

## Blueprints a documenter (priorite SYS-StatSystem)

| Blueprint | Priorite | Notes |
|---|---|---|
| BP_SoM_HeroCharacter | HAUTE | Appelant principal de SetStatValue |
| BP_SoM_PlayerController | HAUTE | OnHeroDied, respawn, inputs |
| BP_SoM_GameMode | HAUTE | OnFountainRest, BPI_Saveable iteration |
| BP_MagicComponent | HAUTE | CastSpell, UnlockDeity, BPI_Saveable |
| BP_ComboManagerComponent | HAUTE | EquipWeapon, InitComboTree, BPI_Saveable |
| BP_CorruptionComponent | MOYENNE | TrackDeityUsage, SetStatValue(Corruption) |
| BP_InventoryComponent | MOYENNE | AddWeapon, GetWeapons, BPI_Saveable |
| BP_EssenceDrop | MOYENNE | SetStatValue(EssenceValue) |
| UI_HUD_Main | MOYENNE | OnStatChanged binding |
| UI_Radial_Main | BASSE | PopulateWeaponSlots, PopulateMagicSchools |

---

## DataTables documentees

| DataTable | Fichier | Dernier snapshot | Statut |
|---|---|---|---|
| DT_StatList | *(a creer)* | -- | MANQUANT |
| DT_Weapons | *(a creer)* | -- | MANQUANT |
| DT_Combo_Sword | *(a creer)* | -- | MANQUANT |
| DT_Deities | *(a creer)* | -- | MANQUANT |
| DT_Spells | *(a creer)* | -- | MANQUANT |

---

## Structs / Enums documentes

| Asset | Fichier | Dernier snapshot | Statut |
|---|---|---|---|
| StatStruct | *(a creer)* | -- | MANQUANT |
| EStatType | *(a creer)* | -- | MANQUANT |
| EElementType | *(a creer)* | -- | MANQUANT |

---

*Derniere mise a jour : 04/06/2026*
