# Index d'Architecture Technique -- Shadow of Mana (ARPG / UE5.7)

---

## Objectif

Table des matieres centrale de toute la documentation technique.
A mettre a jour a chaque creation ou modification de document.

---

## Documents principaux

| Systeme / Module | Document | Statut |
|---|---|---|
| Contexte IA / session | CLAUDE.md (racine) | Mis a jour |
| Presentation generale | Docs/Presentation_Generale_du_Projet.md | A verifier |
| Index architecture (ce doc) | Docs/Project_Architecture_Index.md | Mis a jour |
| Journal des modifications | Docs/Journal_Modifications.md | Mis a jour |
| Roadmap gameplay | Docs/Roadmap_Gameplay.md | Mis a jour |
| Lore | Docs/Lore_ShadowOfMana.md | Stable |
| Sessions UnrealClaude | Docs/Session_UnrealClaude.md | Log continu |

---

## Architecture par module (dossier Docs/Architecture/)

| Module / Systeme | Fichier | Statut |
|---|---|---|
| Index inputs & controles | Input_Architecture.md | Mis a jour 21/05 |
| Radial Menu | RadialMenu_Architecture.md | Mis a jour 21/05 |
| Magic System | Magic_System.md | POC valide |
| Magic Progression | Magic_Progression.md | Design 26/05 |
| Weapons System | Weapons_System_Architecture.md | Stable |
| Combo System | Combo_System_Architecture.md | Stable |
| Stats System | Stats_Architecture.md | Stable |
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
| SaveGame | (a creer -- C1-SaveDesign) | Pas commence |
| Audio | (a creer -- C1-SFXCombat) | Pas commence |
| Quetes | (a creer -- C4-QuestSystem) | Pas commence |
| Dialogue | (a creer -- C4-DialogueSystem) | Pas commence |

---

## Jalons Cycle 1 -- etat synthetique

| Jalon | Statut |
|---|---|
| J-LockOn, J-Camera, J-LockMove, J-TestBed, J-ComboFix | Complets |
| C1-CollisionFix | Complet |
| C1-HitFeel | Partiel (knockback + shake ok, gamepad manque, hitstop reporte) |
| C1-HitFlashEnemies | Abandonne (21/05/2026) |
| C1-CleanupDettes | Partiel (3/4 faits, reste LockOnSwitchCooldown PC) |
| C1-InputsUI | Complet VALIDE PIE (23/05/2026) |
| C1-RadialMagie | Complet VALIDE PIE (25/05/2026) |
| C1-MagicProgressionDesign | Design valide (25/05/2026) |
| C1-MagicDataLayer | Complet VALIDE PIE (25/05/2026) |
| C1-MagicUnlockSystem | A faire -- PRIORITAIRE |
| C1-WeaponArchitecture | A faire |
| C1-SwordMoveset | A faire |
| C1-SaveDesign | A faire |
| C1-BowPOC | A faire |
| C1-WeaponSwitching | A faire |
| C1-SFXCombat | A faire |
| C1-AnimationsPass1 | A faire (fin C1) |

---

## Regles de mise a jour

- Tout ajout de doc = ajouter ici
- Statut = reflete l'etat reel
- Nommage coherent avec les conventions du projet

---

## Historique

- Creation : 17/06/2025
- MAJ 21/05/2026 : resynchro complete, jalons C1 ajoutes, nouveaux fichiers references
- MAJ 26/05/2026 : ajout Magic_Progression.md, mise a jour jalons C1
