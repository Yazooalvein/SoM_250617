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
| BP_SoM_HeroCharacter | [BP_SoM_HeroCharacter.md](BP_SoM_HeroCharacter.md) | 05/06/2026 | Audit global | A JOUR |
| BP_SoM_PlayerController | [BP_SoM_PlayerController.md](BP_SoM_PlayerController.md) | 05/06/2026 | Audit global | A JOUR |
| BP_SoM_GameMode | [BP_SoM_GameMode.md](BP_SoM_GameMode.md) | 05/06/2026 | Audit global | A JOUR |
| BP_AttributeSet_Base | [BP_AttributeSet_Base.md](BP_AttributeSet_Base.md) | 05/06/2026 | Audit global | A JOUR |
| BP_ComboManagerComponent | [BP_ComboManagerComponent.md](BP_ComboManagerComponent.md) | 05/06/2026 | Audit global | A JOUR |
| BP_CombatLockOnComponent | [BP_CombatLockOnComponent.md](BP_CombatLockOnComponent.md) | 05/06/2026 | Audit global | A JOUR |
| BP_MagicComponent | [BP_MagicComponent.md](BP_MagicComponent.md) | 05/06/2026 | Audit global | A JOUR |
| BP_InventoryComponent | [BP_InventoryComponent.md](BP_InventoryComponent.md) | 05/06/2026 | Audit global | A JOUR |
| BP_CorruptionComponent | [BP_CorruptionComponent.md](BP_CorruptionComponent.md) | 05/06/2026 | Audit global | A JOUR |
| BP_EssenceDrop | [BP_EssenceDrop.md](BP_EssenceDrop.md) | 05/06/2026 | Audit global | A JOUR |
| BP_SaveGame_SoM | [BP_SaveGame_SoM.md](BP_SaveGame_SoM.md) | 05/06/2026 | Audit global | A JOUR |
| BP_Fountain_Actor | [BP_Fountain_Actor.md](BP_Fountain_Actor.md) | 05/06/2026 | Audit global | A JOUR |
| BP_FountainComponent | [BP_FountainComponent.md](BP_FountainComponent.md) | 05/06/2026 | Audit global | A JOUR |
| BP_Enemy_Base | [BP_Enemy_Base.md](BP_Enemy_Base.md) | 05/06/2026 | Audit global | A JOUR |
| BP_Enemy_Knight | [BP_Enemy_Knight.md](BP_Enemy_Knight.md) | 05/06/2026 | Audit global | A JOUR |
| BP_AIController_Enemy_Base | [BP_AIController_Enemy_Base.md](BP_AIController_Enemy_Base.md) | 05/06/2026 | Audit global | A JOUR |
| BP_Weapon_Base | [BP_Weapon_Base.md](BP_Weapon_Base.md) | 05/06/2026 | Audit global | A JOUR |
| BP_Spell_Base | [BP_Spell_Base.md](BP_Spell_Base.md) | 05/06/2026 | Audit global | A JOUR |
| BP_Spell_Heal | [BP_Spell_Heal.md](BP_Spell_Heal.md) | 05/06/2026 | Audit global | A JOUR |
| BP_Spell_Attack | [BP_Spell_Attack.md](BP_Spell_Attack.md) | 05/06/2026 | Audit global | A JOUR |
| BP_Spell_Buff | [BP_Spell_Buff.md](BP_Spell_Buff.md) | 05/06/2026 | Audit global | A JOUR |
| BP_Spell_Debuff | [BP_Spell_Debuff.md](BP_Spell_Debuff.md) | 05/06/2026 | Audit global | A JOUR |
| UI_HUD_Main | [UI_HUD_Main.md](UI_HUD_Main.md) | 05/06/2026 | Audit global | A JOUR |
| UI_Radial_Main | [UI_Radial_Main.md](UI_Radial_Main.md) | 05/06/2026 | Audit global | A JOUR |

---

## Blueprints non documentes (peripheriques / tests)

| Blueprint | Raison |
|---|---|
| BP_Enemy_Sword01 | Arme physique ennemie -- pas de variables, overlap -> BPI_TakeDamage |
| BP_Weapon_Sword / BP_Weapon_2HSword | Sous-classes BP_Weapon_Base, variable unique RowName |
| BP_SpellCategoryThresholds | Objet data seul, TMap<E_SpellCategory,int32> |
| BTTask_PerformAttack / BTService_CheckAggroDistance | BT Tasks -- documenter a ENEMY-Types C2 |
| BP_enemyTest / BP_Enemy_TestBed | Assets de test -- hors scope doc |
| BP_Debug_Fountain / BP_Debug_UnlockDeity | Assets debug -- hors scope doc |
| BP_WobbleTarget / BP_JumpPad / BP_DoorFrame | Prototypage niveau -- hors scope doc |
| CS_EnemyDeath / CS_HitReceived | CameraShake -- pas de variables exposees |
| ABP_Manny_Platforming / ABP_Unarmed | AnimBlueprint -- audit visuel UE5 requis |
| CR_Mannequin_* | ControlRig -- hors scope doc |

---

## DataTables documentees

| DataTable | Fichier | Dernier snapshot | Statut |
|---|---|---|---|
| DT_StatList | [DT_StatList.md](DT_StatList.md) | 04/06/2026 | A JOUR (structure partielle) |
| DT_Weapons | *(a creer)* | -- | MANQUANT |
| DT_Combo_Sword | *(a creer)* | -- | MANQUANT |
| DT_Deities | *(a creer)* | -- | MANQUANT |
| DT_Spells | *(a creer)* | -- | MANQUANT |

---

## Structs / Enums documentes

| Asset | Fichier | Dernier snapshot | Statut |
|---|---|---|---|
| StatStruct | [StatStruct.md](../Structs/StatStruct.md) | 04/06/2026 | A JOUR |
| EStatType | [EStatType.md](../Structs/EStatType.md) | 04/06/2026 | PARTIEL |
| EElementType | [EElementType.md](../Structs/EElementType.md) | 04/06/2026 | PARTIEL |

---

## Anomalies detectees -- audit 05/06/2026

| # | BP | Anomalie | Severite | Jalon cible |
|---|---|---|---|---|
| 1 | BP_SoM_HeroCharacter | `bRadialUnlocked` a un espace trailing dans le nom | Moyen | Prochain jalon touchant HC |
| 2 | BP_AttributeSet_Base | `StaminaCurrent` encore en variable native en plus de StatValues | Faible | SYS-Cleanup C2 |
| 3 | BP_AttributeSet_Base | `EssenceValue` et `Corruption` dupliques : native ET StatValues | Faible | SYS-Cleanup C2 |
| 4 | BP_Enemy_Base | `WeaponClass` hardcode en BP_Enemy_Sword01_C* | Dette connue | ENEMY-Types C2 |
| 5 | BP_Enemy_Base | `TriggerHitFlash` present malgre Hit Flash ABANDONNE | Faible | Nettoyage C2 |
| 6 | BP_Enemy_Knight | `EnableWeaponCollision_0` et `EnableWeaponCollision` coexistent | Moyen | ENEMY-Types C2 |
| 7 | BP_SaveGame_SoM | Variable `CurrentSaveGame` auto-referentielle dans le SaveGame | A verifier | Avant prochain SYS-Save |
| 8 | UI_HUD_Main | `PlayerCharacterRef` de type vide (vestige debug) | Faible | UI-HUDPolish C4 |

---

*Derniere mise a jour : 05/06/2026 -- Audit global UnrealClaude (61 assets, 27 BPs details)*
