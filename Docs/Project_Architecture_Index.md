# Index d'Architecture Technique -- Shadow of Mana (ARPG / UE5.7)

---

## Objectif

Table des matieres centrale de toute la documentation technique.
A mettre a jour a chaque creation ou modification de document.

---

## Documents principaux

| Systeme / Module | Document | Statut |
|---|---|---|
| Contexte IA / session | CLAUDE.md (racine) | Mis a jour 09/06/2026 |
| Presentation generale | Docs/Presentation_Generale_du_Projet.md | A verifier |
| Index architecture (ce doc) | Docs/Project_Architecture_Index.md | Mis a jour 09/06/2026 |
| Journal des modifications | Docs/Journal_Modifications.md | Mis a jour 09/06/2026 |
| Roadmap gameplay | Docs/Roadmap_Gameplay.md | Mis a jour 09/06/2026 |
| Planning sessions | Docs/Planning_Sessions.md | A verifier |
| Lore | Docs/Lore_ShadowOfMana.md | Mis a jour 30/05/2026 |
| Sessions UnrealClaude | Docs/Session_UnrealClaude.md | Log continu |

---

## Architecture par module (dossier Docs/Architecture/)

| Module / Systeme | Fichier | Statut |
|---|---|---|
| Decisions architecturales & Patterns | Decisions.md | Mis a jour 03/06/2026 |
| Index inputs & controles | Input_Architecture.md | Mis a jour 21/05 |
| Radial Menu | RadialMenu_Architecture.md | Mis a jour 21/05 |
| Magic System | Magic_System.md | POC valide |
| Magic Progression | Magic_Progression.md | Design 26/05 |
| Weapons System | Weapons_System_Architecture.md | Stable |
| Weapons Progression | Weapons_Progression.md | Design 30/05/2026 |
| Combo System | Combo_System_Architecture.md | Stable |
| Stats System | Stats_Architecture.md | Stable |
| Stats & Progression design | Stats_Progression.md | Mis a jour 29/05/2026 |
| Effets statut & Corruption | Combat_StatusEffects.md | Mis a jour 29/05/2026 |
| Economie & Drops | Economy_Drops.md | Design valide 28/05 |
| Save System & Fontaine de Fee | SaveSystem.md | VALIDE PIE 03/06/2026 |
| Combat System | Combat_Architecture.md | Stable |
| Damage & Collision | Damage_Collision_Architecture.md | Stable |
| Lock-On | LockOn_Architecture.md | Stable |
| HUD | HUD_Architecture.md | Stable |
| UI globale | UI_Architecture.md | A mettre a jour |
| Menus globaux | UI_GlobalMenu.md | A mettre a jour |
| IA globale | AI_Architecture.md | Stable |
| IA ennemis | Enemy_AI_Behavior.md | Stable |
| Ennemi melee | Enemy_MeleeAttack_Architecture.md | Stable |
| Ennemi health bar | Enemy_HealthBar_Architecture.md | Stable |
| Ennemi weapon collision | Enemy_WeaponCollision_And_Damage.md | Stable |
| Animation weapon | Animation_WeaponIntegration.md | Stable |
| Gameplay de base | BasicGameplay_Architecture.md | Stable |
| Audio | (a creer -- AUDIO-C1SFX) | Pas commence |
| Quetes | (a creer -- NAR-QuestSystem C4) | Pas commence |
| Dialogue | (a creer -- NAR-DialogueSystem C4) | Pas commence |

---

## Jalons Cycle 1 -- etat synthetique (09/06/2026)

| Jalon | Statut | Notes C1 |
|---|---|---|
| J-LockOn, J-Camera, J-LockMove, J-TestBed, J-ComboFix | ✅ Complets | -- |
| COMBAT-CollisionFix | ✅ VALIDE PIE | -- |
| COMBAT-HitFeel | Partiel | knockback+shake OK, hitstop reporte C2 |
| COMBAT-HitFlashEnemies | Abandonne (21/05/2026) | -- |
| COMBAT-CleanupDettes | ✅ Complet (27/05/2026) | -- |
| COMBAT-InputsUI | ✅ VALIDE PIE (23/05/2026) | -- |
| MAGIC-RadialMagie | ✅ VALIDE PIE (25/05/2026) | -- |
| MAGIC-ProgressionDesign | ✅ Design valide (25/05/2026) | -- |
| MAGIC-DataLayer | ✅ VALIDE PIE (25/05/2026) | -- |
| MAGIC-UnlockSystem | ✅ VALIDE PIE (27/05/2026) | -- |
| COMBAT-WeaponArchitecture | ✅ VALIDE PIE (29/05/2026) | -- |
| HUD-Core | ✅ VALIDE PIE (31/05/2026) | -- |
| DESIGN-StatsProgression | ✅ Design valide (28/05/2026) | -- |
| DESIGN-StatusEffects | ✅ Design valide (28/05/2026) | -- |
| DESIGN-Corruption | ✅ Design valide (28/05/2026) | -- |
| DESIGN-Economy | ✅ Design valide (28/05/2026) | -- |
| DESIGN-Lore | ✅ Design valide enrichi (30/05/2026) | -- |
| DESIGN-WeaponArchitecture | ✅ Design valide (29/05/2026) | -- |
| DESIGN-WeaponProgression | ✅ Design valide (30/05/2026) | -- |
| DESIGN-SaveDesign | ✅ Design valide (31/05/2026) | -- |
| COMBAT-SwordMoveset | ✅ VALIDE PIE (31/05/2026) | -- |
| SYS-CorruptionSystem | ✅ VALIDE PIE (31/05/2026) | calibrage +5/sort -> SESSION-Economie |
| SYS-EssenceMana | ✅ VALIDE PIE (02/06/2026) | drop au sol C1, mob porteur C2 |
| SYS-SaveGame | ✅ VALIDE PIE (03/06/2026) | BPI_Saveable, LastFountainTransform, overlap auto C1 |
| INFRA-BlueprintSnapshotLayer | ✅ COMPLET (04/06/2026) | -- |
| SYS-StatSystem | ✅ VALIDE PIE (04/06/2026) | TMap stats, Option B GetStatValue |
| ENEMY-DropSystem | ✅ VALIDE PIE (06/06/2026) | BP_EssenceOrb vol auto + BP_ItemDrop stub |
| UI-FountainMenu | ✅ VALIDE PIE (07/06/2026) | BPI_Interactable, mini-menu, SetInputModeUIOnly |
| COMBAT-LockOnRefacto | ✅ VALIDE PIE (09/06/2026) | BPI_Lockable, HP bars hide/show, SwitchLockOnTarget corrige |
| ENEMY-Base | A faire | stats BP_Enemy_Base, HandleTargetDeath |
| ENEMY-Boss1 | A faire | saut + magie placeholder C1 |
| MAP-C1Level | A faire | geometrie BSP/kit C1 |

---

## Regles de mise a jour

- Tout ajout de doc = ajouter ici
- Statut = reflete l'etat reel
- Nommage coherent avec les conventions du projet
- Decisions.md = a lire en debut de session pour respecter les patterns etablis

---

## Historique

- Creation : 17/06/2025
- MAJ 21/05/2026 : resynchro complete, jalons C1 ajoutes
- MAJ 26/05/2026 : ajout Magic_Progression.md, Planning_Sessions.md
- MAJ 29/05/2026 : jalons C1 remis a jour, ajout Stats_Progression.md + Combat_StatusEffects.md + Economy_Drops.md + Decisions.md
- MAJ 30/05/2026 : ajout Weapons_Progression.md
- MAJ 31/05/2026 : ajout SaveSystem.md, DESIGN-SaveDesign valide, HUD-Core complet
- MAJ 02/06/2026 : SYS-EssenceMana VALIDE PIE
- MAJ 03/06/2026 : SYS-SaveGame VALIDE PIE, SaveSystem.md mis a jour
- MAJ 09/06/2026 : SYS-StatSystem, INFRA-BlueprintSnapshotLayer, ENEMY-DropSystem, UI-FountainMenu, COMBAT-LockOnRefacto VALIDE PIE
