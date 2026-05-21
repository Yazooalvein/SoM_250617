# Roadmap Gameplay — Shadow of Mana

Document de référence pour la planification complète du projet.
Mis à jour après chaque session de design ou de développement.

---

## Modules existants (état au 21/05/2026)

| Module | État | Notes |
|--------|------|-------|
| Stats (SetStatValue / OnStatChanged) | ✅ Stable | Architecture solide, ne bougera pas |
| HUD event-driven | ✅ Stable | Zero polling, extensible |
| Iframes dash/roll | ✅ Stable | Via AnimNotify, Dark Souls style |
| Mort du joueur | ✅ Stable | bIsDead + OnPlayerDeath dispatcher |
| Lock-On | ✅ VALIDE PIE | J-LockOn complet + J-LockMove complet |
| Strafe lock-on | ✅ VALIDE PIE | ABP_Manny_Platforming + BS_Unarmed_Strafe (placeholder) |
| Déplacement en lock-on | ✅ VALIDE PIE | Move() via CameraRotation, Rotation Rate -1 |
| Caméra | ✅ VALIDE PIE | SpringArm réglé, IA_Look dans PC, UpdateLockOnRotation V2 |
| Screen shake | ✅ VALIDE PIE | CS_HitReceived + CS_EnemyDeath |
| Knockback ennemi | ✅ VALIDE PIE | LaunchCharacter 400.0 depuis ReceiveDamage |
| Radial menu armes | ✅ Stable | PopulateWeaponSlots, SwitchCategory, ValidateSelectedWeapon |
| Quickslot POC | ✅ POC | 3 slots opérationnels |
| Combo system | ✅ VALIDE PIE | TMap + InitComboTree + LevelMin=0, attaque fonctionnelle |
| IA ennemis | ✅ POC | Behavior Tree + PawnSensing |
| Hit Flash joueur | ✅ Stable | M_Hero HitFlashAmount |
| Hit Flash ennemi | ❌ Abandonné | Decision 21/05 : screen shake + anim suffisent |
| Système de magie | ✅ POC | BP_MagicComponent + 4 sorts Lumina validés PIE |
| Hero placeholder | ✅ PIE | Mesh Meshy + AccuRIG + retargeting Mannequin |
| TestBed | ✅ VALIDE PIE | Lvl_TestBed, BP_Enemy_TestBed, SFX placeholder |
| Collisions capsule | ✅ VALIDE PIE | CapsuleComponent Pawn = Block |
| Radial menu magie | 🔧 En cours | C1-RadialMagie — 2 niveaux (écoles → sorts) |
| IMC_UI dédié menus | 🔧 En cours | C1-InputsUI — PRIORITAIRE |

---

## Vue d'ensemble — Couches de développement

```
COUCHE 1 — Fondations gameplay        (en cours)
COUCHE 2 — Combat & Ennemis           (après fondations)
COUCHE 3 — Monde & Navigation         (en parallèle possible avec C2)
COUCHE 4 — Systèmes narratifs         (après monde + combat)
COUCHE 5 — Forge & Équipement         (après systèmes narratifs)
COUCHE 6 — Audio & Feedback           (C1-SFXCombat en C1, reste intercalé)
COUCHE 7 — UI/UX complet              (intercalé, avant build)
COUCHE 8 — Qualité & Build            (fin de développement)

Sessions créatives (ART / MUS / MAP) : intercalées librement.
```

---

## Ordre de dépendances global (révisé 21/05/2026)

```
[FAIT] J-LockOn -> J-Camera -> J-LockMove -> J-TestBed -> J-ComboFix
  └─> C1-CollisionFix ✅
        └─> C1-HitFeel (partiel : knockback ✅, shake ✅, gamepad ❌, hitstop reporté)
              └─> C1-InputsUI  ← PROCHAIN
                    └─> C1-RadialMagie (radial magie 2 niveaux + fix retour arme équipée)
                          └─> C1-CleanupDettes (supprimer LockOnSwitchCooldown PC)
                                └─> C1-WeaponArchitecture (audit data armes)
                                      └─> C1-SwordMoveset
                                            └─> C1-SaveDesign (spec)
                                                  └─> C1-BowPOC
                                                        └─> C1-WeaponSwitching
                                                              └─> C2-SaveGame
                                                                    └─> C1-AnimationsPass1 (fin C1)

C1-SFXCombat : peut démarrer dès C1-CollisionFix terminé
C1-HitFlashEnemies : ABANDONNE (21/05/2026)

C2-EnemyMesh
  └─> C2-EnemyAI
        └─> C2-EnemyTypes
              └─> C2-Boss1
...
```

---

## COUCHE 1 — Fondations gameplay

### ✅ J-LockOn — Lock-On COMPLET VALIDE PIE (15/05/2026)
### ✅ J-Camera — Caméra & Feel COMPLET VALIDE PIE (17/05/2026)
### ✅ J-LockMove — Déplacement en lock-on COMPLET VALIDE PIE (18/05/2026)
### ✅ J-TestBed — Zone de test COMPLET VALIDE PIE (18/05/2026)
### ✅ J-ComboFix — Fix attaque + combo COMPLET VALIDE PIE (18/05/2026)
### ✅ C1-CollisionFix — Fix collisions capsule COMPLET VALIDE PIE (18/05/2026)

### ❌ C1-HitFlashEnemies — ABANDONNE (21/05/2026)
- Architecture DMI complète mais flash bloqué par M_Mannequin engine (read-only runtime)
- Décision : CS_EnemyDeath (screen shake) + animation dédiée suffisent pour le feedback

### 🔧 C1-HitFeel — Feedback physique des coups (partiel)
- [x] Knockback : LaunchCharacter sur l'ennemi touché VALIDE PIE
- [x] Screen shake polish : CS_HitReceived + CS_EnemyDeath VALIDES PIE
- [ ] Vibration gamepad : hits reçus + mort (standard)
- [ ] Hitstop : reporté après C2-EnemyMesh + C1-SFXCombat

### C1-InputsUI — IMC dédié pour les menus ← PRIORITAIRE
- [ ] Créer IMC_UI séparé (inputs menus séparés des inputs gameplay)
- [ ] Migrer : IA_UI_Radial_Cancel, IA_validate_radial_selection, IA_UI_RadialMenu_ChangeCat
- [ ] Nettoyer IMC_Prototype (inputs gameplay uniquement)
- [ ] Tester switch context gameplay <-> menu (source classique de bugs gamepad)
- [ ] Vérifier que le radial désactive IMC_Prototype et active IMC_UI à l'ouverture
- ⚠️ Prérequis pour C1-RadialMagie

### C1-RadialMagie — Radial magie 2 niveaux + fix arme équipée
- [ ] Fix SelectedIndex à l'ouverture : retourner sur ChoosenWeapon (lookup DiscoveredWeapons) au lieu de 0
- [ ] ERadialMode : vérifier/ajouter valeurs MagicSchool si nécessaire
- [ ] PopulateMagicSchools : lit les écoles disponibles depuis BP_MagicComponent (UnlockedSpells groupés par école)
- [ ] Câbler branche Magic de SwitchCategory : remplacer stub PrintVar par PopulateMagicSchools
- [ ] Sélection école → PopulateMagicSpells(SchoolID) → slots N2
- [ ] ValidateSelectedSpell : CastSpell ou assignation quickslot selon contexte
- [ ] Navigation retour (B) : N2 → N1, N1 → fermer
- [ ] Voir Docs/Architecture/RadialMenu_Architecture.md pour détails techniques
- ⚠️ Nécessite C1-InputsUI

### C1-CleanupDettes — Nettoyage dettes mineures (presque fini)
- [x] Fix TargetActor espace dans UI_LockOnIndicator
- [x] ZOrder=10 sur AddToViewport indicateur lock-on
- [x] Supprimer BT_TestBed et BB_TestBed
- [ ] Supprimer LockOnSwitchCooldown du PC (redondant avec SwitchCooldown du BP_CombatLockOnComponent)
      -> Vérifier que tout le code qui lisait LockOnSwitchCooldown pointe sur Component->SwitchCooldown

### C1-WeaponArchitecture — Audit & décision structure data armes
- [ ] Audit BP_Weapon_Base, DT_Weapons, FWeaponData
- [ ] Décision BP_WeaponType_Base (classe mère abstraite par TYPE)
- [ ] Vérifier champs forge (tier, matériaux, unlock condition) dans FWeaponData
- [ ] Vérifier champs talents (TalentTree ref) dans FWeaponData
- [ ] Doc de décision
- ⚠️ Conditionne C1-SwordMoveset, C1-BowPOC, C5-ForgeSystem, C5-TalentTree

### C1-SwordMoveset — Moveset épée complet
- [ ] Combo 3 coups légers, finisseur, coup chargé (heavy)
- [ ] RotateTowardLockTarget du ComboManager vérifié/câblé avec lock-on
- [ ] Feedback visuel combat : flash arme, posture
- [ ] Épée Mana placeholder
- ⚠️ Nécessite C1-WeaponArchitecture validé

### C1-SaveDesign — Session design : système respawn & sauvegarde
- [ ] Modèle de respawn : sanctuaires DS / checkpoints Seiken-KH / hybride
- [ ] Ce qui est sauvegardé : stats, armes débloquées, sorts, flags narratifs, position
- [ ] Granularité : auto-save + save manuel ? Save slots ?
- [ ] Implications game feel : pénalité mort ? Récupération XP/items ?
- [ ] Livrable : spec SaveGame.md dans Docs/Architecture/

### C1-BowPOC — Arc POC
- [ ] Munitions illimitées
- [ ] Système de visée (lock-on oriente la flèche, visée libre sans lock)
- [ ] Projectile BP, charge optionnelle
- ⚠️ Nécessite C1-WeaponArchitecture validé

### C1-WeaponSwitching — Switching d'armes en combat
- [ ] Switching via radial menu en combat
- [ ] Conservation ou reset combo au switch ?
- [ ] Transition animations entre types d'armes

### C1-SFXCombat — Sons de combat de base
- [ ] Attaques (léger, fort, finisseur), esquive, dash, dégâts reçus, mort joueur + ennemi
- [ ] Sons UI : radial menu, quickslot, validation
- [ ] Sources : packs libres de droits (Free Realistic Sword SFX, 50 Free Game Sounds)
- Peut démarrer dès maintenant (C1-CollisionFix terminé)

### C1-AnimationsPass1 — Premier pass animations (fin de Couche 1)
- [ ] Animations strafe gauche/droite distinctes
- [ ] Roll sans Root Motion en lock-on : LaunchCharacter + animation visuelle
- [ ] Rename ABP_Manny_Platforming -> ABP_Hero
- [ ] Consolidation animations en double
- [ ] Animations de transition (idle -> combat, switch arme)
- ⚠️ Fix roll en lock-on (dette J-LockMove2) inclus ici

---

## COUCHE 2 — Combat & Ennemis

### C2-SaveGame — Implémentation SaveGame
- [ ] BP_SoM_SaveGame (hérite USaveGame)
- [ ] Stats joueur, armes débloquées, sorts débloqués
- [ ] Progression hub, flags narratifs
- [ ] Système respawn selon spec C1-SaveDesign
- ⚠️ Nécessite C1-SaveDesign validé

### C2-EnemyMesh — Mesh ennemis POC
- [ ] Workflow Meshy/AccuRIG pour ennemis
- [ ] Knight ennemi avec vrai mesh (BP_Enemy_Knight)
- [ ] WeaponClass dans BP_Enemy_Base rendu générique
- [ ] Au moins 2 types visuels distincts

### C2-EnemyAI — Révision IA ennemie
- [ ] Révision comportements (aggro, patrouille, désengagement)
- [ ] IA par type d'arme
- [ ] Hitbox précises par type d'attaque

### C2-EnemyTypes — Nouveaux types ennemis
- [ ] Archer, Mage, Colosse

### C2-Boss1 — Premier boss POC
- [ ] Boss Acte 1, 2 phases, attaques spéciales + tells visuels
- [ ] Caméra boss dédiée, musique boss dédiée

---

## COUCHE 3 — Monde & Navigation

### C3-MapTest / C3-MapHub / C3-MapStart / C3-Flammy / C3-ZoneTransition

---

## COUCHE 4 — Systèmes Narratifs & Progression

### C4-DialogueSystem / C4-Tutorial / C4-DeitiesSystem / C4-CorruptionSystem
### C4-MoralFlag / C4-HubState1/2/3 / C4-Companions / C4-QuestSystem
### C4-LoreCodex / C4-SisterReveal

---

## COUCHE 5 — Forge & Équipement

### C5-ForgeSystem / C5-Equipment / C5-TalentTree

---

## COUCHE 6 — Audio & Feedback

### C6-SFXAmbiance / C6-SFXMagic / C6-Music1/2/3 / C6-AudioMix

---

## COUCHE 7 — UI/UX Complet

### C7-MainMenu / C7-OptionsMenu / C7-PauseMenu / C7-DeathScreen / C7-LoadingScreen
### C7-HUDPolish / C7-Localization

---

## COUCHE 8 — Qualité & Build

### C8-DebugPanel / C8-Act1Playtest / C8-Perf1/2 / C8-CrashSession / C8-Build1/2

---

## Sessions Créatives

| Session | Contenu |
|---------|---------|
| ART-Hero | LODs + correction 6 doigts + sockets (retopo 246K -> 10-15K) |
| ART-Enemies | Meshes ennemis (Knight + 1-2 types) |
| ART-Weapons | Assets armes (Sword_01, 2HSword_01, Arc_01...) |
| ART-NPC | Lumina, Luna, Athanor placeholders |
| MAP-Test/Hub/Start | Maps terrain UE5 |
| MUS-1/2/3 | Thèmes musicaux (workflow Suno établi) |

---

## Points de Design Encore Ouverts

| Sujet | Lié à |
|-------|-------|
| Modèle respawn : sanctuaires DS / checkpoints Seiken-KH / hybride | C1-SaveDesign |
| Switching armes : reset combo ou conservation ? | C1-WeaponSwitching |
| Forge : matériaux exacts (graines Mana ?) | C5-ForgeSystem |
| Corruption : les sorts de soin corrompent-ils moins ? | C4-CorruptionSystem |
| Compagnons : mort permanente possible hors choix moral ? | C4-Companions |
| Garçon Loup : Salamandre ou Gnome ? | C4-DeitiesSystem |
| Colosse : Gnome confirmé ? | C4-DeitiesSystem |
| Flammy : quel jalon narratif débloque le voyage rapide ? | C3-Flammy |
| Touchpad PS5 : carte, journal, ou autre ? | C7-PauseMenu |
| Menu pause : Time Dilation 0 ou pause complète ? | C7-PauseMenu |
| Quickslot switch : press = utiliser, hold = changer de page ? | C1-InputsUI |
| Radial Magie N2 : validation = CastSpell ou assignation quickslot ? | C1-RadialMagie |
| Distribution future : Steam / itch.io / perso | C8-Build2 |

---

## Historique

- Création : 11/05/2026
- Refonte complète : 14/05/2026
- Resynchro complète : 18/05/2026
- MAJ 21/05/2026 : C1-HitFlashEnemies abandonné, C1-RadialMagie ajouté, C1-InputsUI priorisé, CleanupDettes partiel, ordre jalons révisé
