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
| BP_AttributeSet_Base | [BP_AttributeSet_Base.md](BP_AttributeSet_Base.md) | 04/06/2026 | SYS-StatSystem pre-audit | A JOUR |
| BP_SoM_HeroCharacter | [BP_SoM_HeroCharacter.md](BP_SoM_HeroCharacter.md) | 04/06/2026 | SYS-StatSystem pre-audit | A JOUR |
| BP_SoM_PlayerController | [BP_SoM_PlayerController.md](BP_SoM_PlayerController.md) | 04/06/2026 | SYS-StatSystem pre-audit | A JOUR |
| BP_SoM_GameMode | [BP_SoM_GameMode.md](BP_SoM_GameMode.md) | 04/06/2026 | SYS-StatSystem pre-audit | A JOUR |
| BP_MagicComponent | [BP_MagicComponent.md](BP_MagicComponent.md) | 04/06/2026 | SYS-StatSystem pre-audit | A JOUR |
| BP_CorruptionComponent | [BP_CorruptionComponent.md](BP_CorruptionComponent.md) | 04/06/2026 | SYS-StatSystem pre-audit | A JOUR |
| BP_EssenceDrop | [BP_EssenceDrop.md](BP_EssenceDrop.md) | 04/06/2026 | SYS-StatSystem pre-audit | A JOUR |
| BP_Spell_Heal | [BP_Spell_Heal.md](BP_Spell_Heal.md) | 04/06/2026 | SYS-StatSystem pre-audit | A JOUR |
| BP_Spell_Buff | [BP_Spell_Buff.md](BP_Spell_Buff.md) | 04/06/2026 | SYS-StatSystem pre-audit | A JOUR |
| UI_HUD_Main | [UI_HUD_Main.md](UI_HUD_Main.md) | 04/06/2026 | SYS-StatSystem pre-audit | A JOUR |

---

## Blueprints a documenter (jalons suivants)

| Blueprint | Priorite | Notes |
|---|---|---|
| BP_ComboManagerComponent | HAUTE | EquipWeapon, InitComboTree, BPI_Saveable -- MAGIC-TreeModule |
| BP_InventoryComponent | HAUTE | AddWeapon, GetWeapons, BPI_Saveable -- MAGIC-TreeModule |
| UI_Radial_Main | MOYENNE | PopulateWeaponSlots, PopulateMagicSchools |
| BP_Enemy_Base | MOYENNE | Stats -- ENEMY-Base |

---

## DataTables documentees

| DataTable | Fichier | Dernier snapshot | Statut |
|---|---|---|---|
| DT_StatList | [DT_StatList.md](DT_StatList.md) | 04/06/2026 | A JOUR (structure partielle -- rows non listables via MCP) |
| DT_Weapons | *(a creer)* | -- | MANQUANT |
| DT_Combo_Sword | *(a creer)* | -- | MANQUANT |
| DT_Deities | *(a creer)* | -- | MANQUANT |
| DT_Spells | *(a creer)* | -- | MANQUANT |

---

## Structs / Enums documentes

| Asset | Fichier | Dernier snapshot | Statut |
|---|---|---|---|
| StatStruct | [StatStruct.md](../Structs/StatStruct.md) | 04/06/2026 | A JOUR (infere depuis nodes) |
| EStatType | [EStatType.md](../Structs/EStatType.md) | 04/06/2026 | PARTIEL (MCP non accessible -- audit visuel requis) |
| EElementType | [EElementType.md](../Structs/EElementType.md) | 04/06/2026 | PARTIEL (MCP non accessible -- audit visuel requis) |

---

*Derniere mise a jour : 04/06/2026*
