# Index d'Architecture Technique -- Shadow of Mana (ARPG / UE5.7)

---

## Objectif

Table des matieres centrale de toute la documentation technique.
A mettre a jour a chaque creation ou modification de document.

---

## Documents principaux

| Systeme / Module | Document | Statut |
|---|---|---|
| Contexte IA / session | CLAUDE.md (racine) | Mis a jour 31/05/2026 |
| Presentation generale | Docs/Presentation_Generale_du_Projet.md | A verifier |
| Index architecture (ce doc) | Docs/Project_Architecture_Index.md | Mis a jour 31/05/2026 |
| Journal des modifications | Docs/Journal_Modifications.md | Mis a jour 31/05/2026 |
| Roadmap gameplay | Docs/Roadmap_Gameplay.md | Mis a jour 29/05/2026 |
| Planning sessions | Docs/Planning_Sessions.md | A verifier |
| Lore | Docs/Lore_ShadowOfMana.md | Mis a jour 30/05/2026 |
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
| Weapons Progression | Weapons_Progression.md | Design 30/05/2026 |
| Combo System | Combo_System_Architecture.md | Stable |
| Stats System | Stats_Architecture.md | Stable |
| Stats & Progression design | Stats_Progression.md | Mis a jour 29/05/2026 |
| Effets statut & Corruption | Combat_StatusEffects.md | Mis a jour 29/05/2026 |
| Economie & Drops | Economy_Drops.md | Design valide 28/05 |
| Save System & Fontaine de Fee | SaveSystem.md | Design valide 31/05/2026 |
| Decisions architecturales | Decisions.md | Mis a jour 29/05/2026 |
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
| Audio | (a creer -- C1-SFXCombat) | Pas commence |
| Quetes | (a creer -- C4-QuestSystem) | Pas commence |
| Dialogue | (a creer -- C4-DialogueSystem) | Pas commence |

---

## Jalons Cycle 1 -- etat synthetique (31/05/2026)

| Jalon | Statut |
|---|---|
| J-LockOn, J-Camera, J-LockMove, J-TestBed, J-ComboFix | ✅ Complets |
| C1-CollisionFix | ✅ Complet VALIDE PIE |
| C1-HitFeel | 🔧 Partiel (knockback + shake OK, gamepad manque, hitstop reporte) |
| C1-HitFlashEnemies | ❌ Abandonne (21/05/2026) |
| C1-CleanupDettes | ✅ Complet (27/05/2026) |
| C1-InputsUI | ✅ Complet VALIDE PIE (23/05/2026) |
| C1-RadialMagie | ✅ Complet VALIDE PIE (25/05/2026) |
| C1-MagicProgressionDesign | ✅ Design valide (25/05/2026) |
| C1-MagicDataLayer | ✅ Complet VALIDE PIE (25/05/2026) |
| C1-MagicUnlockSystem | ✅ Complet VALIDE PIE (27/05/2026) |
| C1-WeaponArchitecture + Refacto | ✅ Complet VALIDE PIE (29/05/2026) |
| C1-HUDCore | ✅ Complet VALIDE PIE (31/05/2026) |
| DESIGN-StatsProgression | ✅ Design valide (28/05/2026) |
| DESIGN-StatusEffects | ✅ Design valide (28/05/2026) |
| DESIGN-Corruption | ✅ Design valide (28/05/2026) |
| DESIGN-Economy | ✅ Design valide (28/05/2026) |
| DESIGN-Lore | ✅ Design valide enrichi (30/05/2026) |
| DESIGN-WeaponArchitecture | ✅ Design valide (29/05/2026) |
| DESIGN-WeaponProgression | ✅ Design valide (30/05/2026) |
| DESIGN-SaveDesign | ✅ Design valide (31/05/2026) |
| C1-BowPOC | ⏳ A faire |
| C1-WeaponSwitching | ⏳ A faire |
| C1-SFXCombat | ⏳ A faire |
| C1-MagicTreeModule | ⏳ A faire |
| C1-AnimationsPass1 | ⏳ A faire (fin C1) |

---

## Regles de mise a jour

- Tout ajout de doc = ajouter ici
- Statut = reflete l'etat reel
- Nommage coherent avec les conventions du projet

---

## Historique

- Creation : 17/06/2025
- MAJ 21/05/2026 : resynchro complete, jalons C1 ajoutes, nouveaux fichiers references
- MAJ 26/05/2026 : ajout Magic_Progression.md, Planning_Sessions.md, Lore mis a jour
- MAJ 29/05/2026 : jalons C1 remis a jour (C1-WeaponArchitecture complet, tous DESIGN valides), ajout Stats_Progression.md + Combat_StatusEffects.md + Economy_Drops.md + Decisions.md dans index, dates mises a jour
- MAJ 30/05/2026 : ajout Weapons_Progression.md, DESIGN-WeaponProgression valide
- MAJ 31/05/2026 : ajout SaveSystem.md, DESIGN-SaveDesign valide, C1-HUDCore complet, jalons mis a jour
