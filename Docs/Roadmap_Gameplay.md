# Roadmap Gameplay — Shadow of Mana

Document de référence pour la planification complète du projet.
Mis à jour après chaque session de design ou de développement.

---

## Modules existants (état au 18/05/2026)

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
| Radial menu unifié | ✅ Stable | Complet + nettoyage propre |
| Quickslot POC | ✅ POC | 3 slots opérationnels |
| Combo system | ✅ VALIDE PIE | TMap + InitComboTree + LevelMin=0, attaque fonctionnelle |
| IA ennemis | ✅ POC | Behavior Tree + PawnSensing |
| Hit Flash joueur | ✅ Stable | M_Hero HitFlashAmount |
| Hit Flash ennemi | ⚠️ À faire | C1-HitFlashEnemies prévu |
| Système de magie | ✅ POC | BP_MagicComponent + 4 sorts Lumina validés PIE |
| Hero placeholder | ✅ PIE | Mesh Meshy + AccuRIG + retargeting Mannequin |
| TestBed | ✅ VALIDE PIE | Lvl_TestBed, BP_Enemy_TestBed, SFX placeholder |
| Collisions capsule/physique | ❌ Bug | Pawns se traversent, coups sans feedback — C1-CollisionFix |

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

## Ordre de dépendances global (révisé 18/05/2026)

```
[FAIT] J-LockOn -> J-Camera -> J-LockMove -> J-TestBed -> J-ComboFix
  └─> C1-CollisionFix (bug bloquant pour les tests combat)
        └─> C1-HitFlashEnemies (quickwin)
              └─> C1-HitFeel (knockback + hitstop + screen shake polish)
                    └─> C1-InputsUI (IMC dédié menus)
                          └─> C1-WeaponArchitecture (audit data pour forge/talents)
                                └─> C1-SwordMoveset (moveset épée complet)
                                      └─> C1-SaveDesign (session design respawn/save)
                                            └─> C1-BowPOC (arc)
                                                  └─> C1-WeaponSwitching
                                                        └─> C2-SaveGame (implémentation)
                                                              └─> C1-AnimationsPass1

C1-SFXCombat : sons combat de base — peut démarrer après C1-CollisionFix
C1-CleanupDettes : dettes mineures — session rapide, intercalable

C2-EnemyMesh
  └─> C2-EnemyAI
        └─> C2-EnemyTypes
              └─> C2-Boss1

C3-MapTest (apprentissage Landscape)
  └─> C4-DialogueSystem
        └─> C3-MapHub + C3-MapStart
              └─> C4-DeitiesSystem
                    └─> C4-CorruptionSystem
                          └─> C4-MoralFlag
                                └─> C4-HubState1/2/3
                                      └─> C8-Act1Playtest

C8-Act1Playtest
  └─> C8-Perf1
        └─> C8-Build1
              └─> C8-Build2
```

---

## COUCHE 1 — Fondations gameplay

### ✅ J-LockOn — Lock-On COMPLET VALIDE PIE (15/05/2026)
- [x] Fix IsLockOnActive (retournait vide)
- [x] Fix espace dans dispatcher OnLockOnDeactivated
- [x] Bindings OnLockOnActivated/Deactivated dans BP_SoM_HeroCharacter
- [x] bOrientRotationToMovement + UseControllerRotationYaw corrects
- [x] Strafe fonctionnel PIE (ABP_Manny_Platforming + BS_Unarmed_Strafe)
- [x] Indicateur lock : SetVisibility selon frustum
- [x] Edge cases : mort ennemi, switch cible, délock manuel, délock hors range

### ✅ J-Camera — Caméra & Feel COMPLET VALIDE PIE (17/05/2026)
- [x] SpringArm réglé (Arm 350, OffsetZ 60, Lag 8, MaxDist 200)
- [x] IA_Look déplacé dans BP_SoM_PlayerController (fonction Aim)
- [x] UpdateLockOnRotation V2 (conditionnel, bPlayerIsLooking, LookReturnDelay)
- [x] Screen shake : CS_HitReceived + CS_EnemyDeath VALIDES PIE
- [x] Fix PlayerCharacterRef SET au OnPossess

### ✅ J-LockMove — Déplacement en lock-on COMPLET VALIDE PIE (18/05/2026)
- [x] Move() via GetPlayerCameraManager -> GetCameraRotation en lock-on
- [x] LastAxisX / LastAxisY stockés au Triggered de IA_Move
- [x] Rotation Rate Z = -1 (pivot instantané hors lock-on)
- ⚠️ Dette : roll en lock-on part vers l'ennemi (Root Motion) -> C1-AnimationsPass1

### ✅ J-TestBed — Zone de test COMPLET VALIDE PIE (18/05/2026)
- [x] Lvl_TestBed : BSP 4000x4000, NavMesh, lighting Movable, GameMode Override
- [x] BP_Enemy_TestBed : stats Instance Editable, hérite BP_Enemy_Base
- [x] SFX placeholder : hit joueur, attaque ennemi, roll hero

### ✅ J-ComboFix — Fix attaque + combo COMPLET VALIDE PIE (18/05/2026)
- [x] SET ChoosenWeapon dans EquipWeapon
- [x] InitComboTree appelé à l'équipement
- [x] HandleAttack : suppression paramètre ChoosenWeapon (ComboManager lit CurrentWeaponID)
- [x] LevelMin = 0 sur toutes les rows DT_Combo

---

### C1-CollisionFix — Fix collisions capsule & réaction physique
**Priorité : HAUTE — bloquant pour les tests combat**
- [ ] Diagnostic : Capsule Collision Channel sur BP_Enemy_Base et BP_SoM_HeroCharacter
- [ ] Fix pawns qui se traversent (Block sur Pawn channel)
- [ ] Réglage Collision Preset cohérent entre Hero, ennemis, armes
- [ ] Vérifier que les WeaponCollision boxes ne persistent pas entre frames
- ⚠️ Prérequis pour C1-HitFeel

### C1-HitFlashEnemies — Hit Flash ennemis (quickwin)
- [ ] DMI (Dynamic Material Instance) au BeginPlay sur BP_Enemy_Base
- [ ] M_Enemy_Base avec paramètre HitFlashAmount
- [ ] Appel SetScalarParameterValue dans ReceiveDamage ennemi
- [ ] Test sur BP_Enemy_TestBed dans Lvl_TestBed

### C1-HitFeel — Feedback physique des coups
**Absorbe la dette screen shake existante**
- [ ] Knockback : LaunchCharacter sur l'ennemi touché (direction + force)
- [ ] Hitstop : Game Time Dilation 0.05 pendant 2-3 frames sur coup fort
- [ ] Screen shake polish : ajuster CS_HitReceived et CS_EnemyDeath si nécessaire
- [ ] Vibration gamepad : hits reçus + mort (standard, pas haptique avancé)
- ⚠️ Nécessite C1-CollisionFix

### C1-CleanupDettes — Nettoyage dettes mineures (session rapide ~1h)
- [ ] Unifier doublon cooldown switch : LockOnSwitchCooldown (PC) + SwitchCooldown (Component)
- [ ] Fix TargetActor espace dans UI_LockOnIndicator ("TargetActor ")
- [ ] ZOrder=10 sur AddToViewport de l'indicateur lock-on
- [ ] Supprimer BT_TestBed et BB_TestBed (créés puis abandonnés)
- [ ] Rename ABP_Manny_Platforming -> ABP_Hero (si pas fait en C1-AnimationsPass1)

### C1-InputsUI — IMC dédié pour les menus
- [ ] Créer IMC_UI séparé (inputs menus séparés des inputs gameplay)
- [ ] Migrer : IA_UI_Radial_Cancel, IA_validate_radial_selection, IA_UI_RadialMenu_ChangeCat
- [ ] Nettoyer IMC_Prototype (inputs gameplay uniquement)
- [ ] Tester switch context gameplay <-> menu (source classique de bugs gamepad)

### C1-WeaponArchitecture — Audit & décision structure data armes
**Objectif : valider ou renforcer les fondations avant forge/talents**
- [ ] Audit BP_Weapon_Base, DT_Weapons, FWeaponData : la structure actuelle tient-elle jusqu'à la forge ?
- [ ] Décision BP_WeaponType_Base (classe mère abstraite par TYPE) : nécessaire ou non ?
- [ ] Vérifier que DT_Weapons peut accueillir les champs forge (tier, matériaux requis, unlock condition)
- [ ] Vérifier que FWeaponData peut accueillir les champs talents (TalentTree ref)
- [ ] Doc de décision : ce qui change, ce qui reste
- ⚠️ Conditionne C1-SwordMoveset, C1-BowPOC, C5-ForgeSystem, C5-TalentTree

### C1-SwordMoveset — Moveset épée complet
- [ ] Combo 3 coups légers, finisseur, coup chargé (heavy)
- [ ] RotateTowardLockTarget du ComboManager vérifié/câblé avec lock-on
- [ ] Feedback visuel combat : flash arme, posture — PAS d'UI visible (ACTÉ)
- [ ] Épée Mana placeholder (asset narratif, sera upgradé via forge)
- ⚠️ Nécessite C1-WeaponArchitecture validé

### C1-SaveDesign — Session design : système respawn & sauvegarde
**Session design pure — pas de code, une spec validée en sortie**
- [ ] Décider le modèle de respawn : sanctuaires DS / checkpoints Seiken-KH / hybride
- [ ] Définir ce qui est sauvegardé : stats, armes débloquées, sorts, flags narratifs, position ?
- [ ] Définir la granularité : auto-save + save manuel ? Save slots ?
- [ ] Implications sur le game feel : pénalité mort ? Récupération XP/items ?
- [ ] Livrable : spec SaveGame.md dans Docs/Architecture/

### C1-BowPOC — Arc POC
- [ ] Munitions illimitées (ACTÉ)
- [ ] Système de visée (lock-on oriente la flèche, visée libre sans lock)
- [ ] Projectile BP, charge optionnelle
- ⚠️ Nécessite C1-WeaponArchitecture validé

### C1-WeaponSwitching — Switching d'armes en combat
- [ ] Switching via radial menu en combat
- [ ] Conservation ou reset combo au switch ? (point ouvert — à trancher en C1-SaveDesign ou séparément)
- [ ] Transition animations entre types d'armes

### C1-SFXCombat — Sons de combat de base
- [ ] Attaques (léger, fort, finisseur), esquive, dash, dégâts reçus, mort joueur + ennemi
- [ ] Sons UI : radial menu, quickslot, validation
- [ ] Sources : packs libres de droits déjà identifiés (Free Realistic Sword SFX, 50 Free Game Sounds)
- Peut démarrer dès C1-CollisionFix terminé

### C1-AnimationsPass1 — Premier pass animations (hors placeholder)
**À placer en fin de Couche 1 — les placeholders suffisent jusque-là**
- [ ] Animations strafe gauche/droite distinctes (placeholder actuel = Jog_Left x2)
- [ ] Roll sans Root Motion en lock-on : LaunchCharacter + animation visuelle (fix C1-LockMove2)
- [ ] Rename ABP_Manny_Platforming -> ABP_Hero
- [ ] Consolidation animations en double
- [ ] Animations de transition (idle -> combat, switch arme)
- ⚠️ Fix roll en lock-on (dette J-LockMove2) inclus ici

---

## COUCHE 2 — Combat & Ennemis

### C2-SaveGame — Implémentation SaveGame
**Implémentation de la spec définie en C1-SaveDesign**
- [ ] BP_SoM_SaveGame (hérite USaveGame)
- [ ] Stats joueur, armes débloquées, sorts débloqués
- [ ] Progression hub, flags narratifs (dont flag Général / bGeneralSpared)
- [ ] Système respawn selon spec C1-SaveDesign
- ⚠️ Nécessite C1-SaveDesign (spec) validé

### C2-EnemyMesh — Mesh ennemis POC
- [ ] Workflow Meshy/AccuRIG pour ennemis (même pipeline que héros)
- [ ] Knight ennemi avec vrai mesh (BP_Enemy_Knight)
- [ ] WeaponClass dans BP_Enemy_Base rendu générique (actuellement hardcodé BP_Enemy_Sword01)
- [ ] Material ennemi + Hit Flash (si pas fait en C1-HitFlashEnemies)
- [ ] Au moins 2 types visuels distincts

### C2-EnemyAI — Révision IA ennemie
- [ ] Révision comportements (aggro, patrouille, désengagement)
- [ ] IA par type d'arme (épée vs archer vs mage)
- [ ] Hitbox précises par type d'attaque
- [ ] BTService_CheckAggroDistance : révision radius + conditions

### C2-EnemyTypes — Nouveaux types ennemis
- [ ] Archer, Mage, Colosse — chacun héritant BP_Enemy_Base

### C2-Boss1 — Premier boss POC
- [ ] Boss Acte 1, 2 phases, attaques spéciales + tells visuels
- [ ] Caméra boss dédiée, musique boss dédiée

---

## COUCHE 3 — Monde & Navigation

### C3-MapTest — Map de test réelle (apprentissage Landscape)
- [ ] Landscape, foliage, lighting, collisions
- [ ] Zone forêt ou ruines, pas de finition artistique

### C3-MapHub — Ville de l'Oracle (Hub Acte 1)
- [ ] Layout de base, éclairage, navigation IA, points PNJ

### C3-MapStart — Ville Détruite du Héros (zone de départ)
- [ ] Zone linéaire courte, tutoriel naturel

### C3-Flammy — Système de voyage rapide
- [ ] BP_Flammy, points débloqués progressivement, dialogues courts

### C3-ZoneTransition — Transitions entre zones
- [ ] Chargement entre niveaux, persistance état joueur

---

## COUCHE 4 — Systèmes Narratifs & Progression

### C4-DialogueSystem — Système de dialogues
- [ ] DT_Dialogues (FR/EN), widget dialogue, déclencheurs, StringTable

### C4-Tutorial — Tutoriel in-game
- [ ] Hints contextuels minimalistes, premiers instants uniquement, désactivables

### C4-DeitiesSystem — Toutes les déités (session groupée)
- [ ] Lumina (fait) -> intégration narrative
- [ ] Luna, Ombre, Sylphide, Gnome, Salamandre, Athanor, Ondine, Dryade
- [ ] Chaque déité = 4 sorts (attaque, buff, soin, ultime)
- [ ] Arbres de talents auront une incidence sur les sorts

### C4-CorruptionSystem — Système de corruption magique
- [ ] BP_CorruptionComponent (0-100), effets par seuil 25/50/75/100
- [ ] Indicateur HUD minimal, sanctuaires de purification

### C4-MoralFlag — Flag Général de l'Empire
- [ ] bGeneralSpared dans SaveGame, conséquences Acte 4

### C4-HubState1 / C4-HubState2 / C4-HubState3 — Ville de l'Oracle états 1-2-3
- [ ] PNJ, dialogues, forge, HubProgressionLevel, Flammy

### C4-Companions — Luna, Lumina, Loup & Colosse

### C4-QuestSystem — Système de quêtes
- [ ] DT_Quests, BP_QuestManager, suivi dans menu pause

### C4-LoreCodex — Codex lore débloquable
- [ ] DT_Lore, widget codex dans menu pause

### C4-SisterReveal — Révélation narrative (Acte 3)
- [ ] Sequencer UE5, divergence selon flag bGeneralSpared

---

## COUCHE 5 — Forge & Équipement

### C5-ForgeSystem — BP_ForgeComponent + évolution armes
- [ ] Interface forge, NPC Athanor, conditions narratives de déblocage
- [ ] Épée -> Flamberge -> Katana, Arc -> Arc long -> Arbalète -> Arc elfique
- ⚠️ Nécessite C1-WeaponArchitecture validé

### C5-Equipment — Système d'équipement
- [ ] Bonus % stats, intégré SetStatValue, affiché menu pause

### C5-TalentTree — Arbre de talent par type d'arme
- [ ] DT_Talents + BP_TalentManager, incidence sur sorts déités
- ⚠️ Nécessite C1-WeaponArchitecture validé

---

## COUCHE 6 — Audio & Feedback

*C1-SFXCombat remonté en Couche 1.*

### C6-SFXAmbiance — Ambiances par zone
### C6-SFXMagic — Sons de magie
### C6-Music1 / C6-Music2 / C6-Music3 — Thèmes musicaux
### C6-AudioMix — Mixage global

---

## COUCHE 7 — UI/UX Complet

### C7-MainMenu / C7-OptionsMenu / C7-PauseMenu / C7-DeathScreen / C7-LoadingScreen
### C7-HUDPolish — Icônes quickslot, indicateur corruption, boussole légère
### C7-Localization — FR/EN (StringTable, pas de hardcode)

---

## COUCHE 8 — Qualité & Build

### C8-DebugPanel — Panneau debug in-game (désactivé en release)
### C8-Act1Playtest — Map test Acte 1 jouable (30-45 min de jeu)
### C8-Perf1 / C8-Perf2 — Profiling + optimisation (cible 60 FPS)
### C8-CrashSession — Session edge cases
### C8-Build1 — Build packagée Windows
### C8-Build2 — Verticale slice Acte 1

---

## Sessions Créatives (intercalées librement)

| Session | Contenu |
|---------|---------|
| ART-Hero | LODs + correction 6 doigts + sockets affinés (retopo 246K -> 10-15K) |
| ART-Enemies | Meshes ennemis (Knight + 1-2 types) |
| ART-Weapons | Assets armes séparés (Sword_01, 2HSword_01, Arc_01...) |
| ART-NPC | Lumina, Luna, Athanor placeholders |
| MAP-Test | Map terrain UE5 (apprentissage) |
| MAP-Hub | Ville de l'Oracle |
| MAP-Start | Ville Détruite du Héros |
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
| Distribution future : Steam / itch.io / perso | C8-Build2 |

---

## Historique

- Création : 11/05/2026
- Refonte complète : 14/05/2026
- Resynchro complète : 18/05/2026 — jalons complétés cochés, renommage convention C1/C2.., nouveaux jalons C1-CollisionFix / C1-HitFeel / C1-HitFlashEnemies / C1-SaveDesign / C2-SaveGame / C1-WeaponArchitecture / C1-CleanupDettes
