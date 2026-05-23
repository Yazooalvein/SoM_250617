# Roadmap Gameplay — Shadow of Mana

Document de référence pour la planification complète du projet.
Mis à jour après chaque session de design ou de développement.

---

## Modules existants (état au 23/05/2026)

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
| IMC dédiés (5 contextes) | ✅ VALIDE PIE | C1-InputsUI complet -- swap OpenRadial/CloseRadial |
| Radial menu magie | 🔧 À faire | C1-RadialMagie — 2 niveaux (écoles → sorts) |

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

## Ordre de dépendances global (révisé 23/05/2026)

```
[FAIT] J-LockOn -> J-Camera -> J-LockMove -> J-TestBed -> J-ComboFix
  └─> C1-CollisionFix ✅
        └─> C1-HitFeel (partiel : knockback ✅, shake ✅, gamepad ❌, hitstop reporté)
              └─> C1-InputsUI ✅ VALIDE PIE
                    └─> C1-RadialMagie (radial magie 2 niveaux)  ← PROCHAIN
                          └─> C1-MagicProgressionDesign (spec design : montée de niveau sorts)
                                └─> C1-CleanupDettes (LockOnSwitchCooldown PC + SelectedIndex radial)
                                      └─> C1-WeaponArchitecture
                                            └─> C1-SwordMoveset
                                                  └─> C1-SaveDesign (spec)
                                                        └─> C1-BowPOC
                                                              └─> C1-WeaponSwitching
                                                                    └─> C2-SaveGame
                                                                          └─> C1-AnimationsPass1 (fin C1)

C1-SFXCombat : peut démarrer dès maintenant
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
- Décision : CS_EnemyDeath (screen shake) + animation dédiée suffisent

### 🔧 C1-HitFeel — Feedback physique des coups (partiel)
- [x] Knockback VALIDE PIE
- [x] Screen shake VALIDE PIE
- [ ] Vibration gamepad
- [ ] Hitstop : reporté après C2-EnemyMesh + C1-SFXCombat

### ✅ C1-InputsUI — IMC dédiés COMPLET VALIDE PIE (23/05/2026)
- [x] IMC_Gameplay (ex IMC_Prototype) : charge au ReceivePossessed HeroCharacter
- [x] IMC_Radial : 4 IA, swap dans OpenRadial/CloseRadial
- [x] Stubs vides : IMC_Menu (C7), IMC_Dialogue (C4), IMC_Cutscene (C3)
- [x] Fix rotation : trigger Pressed threshold 0.5 + Modifier Negate X direction gauche
- [x] Tests PIE : gameplay bloqué pendant radial, repris après fermeture

### C1-RadialMagie — Radial magie 2 niveaux ← PROCHAIN
**Décisions actées (23/05/2026) :**
- Validation N2 = CastSpell direct (assignation quickslot = menu général hors combat)
- Source écoles = filtrage UnlockedSpells par Category (pas de variable UnlockedSchools)
- SelectedIndex arme au retour = reporté en C1-CleanupDettes

**Tâches :**
- [ ] PopulateMagicSchools : loop UnlockedSpells -> extract Category -> dedup -> slots N1
- [ ] Câbler branche Magic de SwitchCategory (remplacer stub PrintVar)
- [ ] Sélection école + confirmer A -> PopulateMagicSpells(SchoolID) -> slots N2
- [ ] ValidateSelectedSpell : CastSpell(SpellID) via MagicComponent -> CloseRadial
- [ ] Navigation retour B : N2 -> N1, N1 -> fermer
- [ ] Variable CurrentMagicSchool (FName) dans UI_Radial_Main : ecole selectionnee en N1
- [ ] Text_Category : afficher "MAGIE - [NomEcole]" en N2, "MAGIE" en N1
- ⚠️ Nécessite C1-InputsUI ✅

### C1-MagicProgressionDesign — Session design progression des sorts
- [ ] Trancher : montée de niveau linéaire (puissance/durée) vs arbre de talent par sort
- [ ] Cohérence avec progression armes (forge + talents)
- [ ] Décider si les ennemis magiques partagent DT_Spells du hero ou sous-ensemble dédié
- [ ] Livrable : spec MagicProgression.md
- ⚠️ Aucune implémentation avant cette session

### C1-CleanupDettes — Nettoyage dettes mineures (presque fini)
- [x] Fix TargetActor espace dans UI_LockOnIndicator
- [x] ZOrder=10 sur AddToViewport indicateur lock-on
- [x] Supprimer BT_TestBed et BB_TestBed
- [ ] Supprimer LockOnSwitchCooldown du PC (redondant avec Component->SwitchCooldown)
- [ ] SelectedIndex radial : retourner sur ChoosenWeapon à l'ouverture (FindIndex dans DiscoveredWeapons)

### C1-WeaponArchitecture — Audit & décision structure data armes
- [ ] Audit BP_Weapon_Base, DT_Weapons, FWeaponData
- [ ] Décision BP_WeaponType_Base (classe mère abstraite par TYPE)
- [ ] Vérifier champs forge + talents dans FWeaponData
- [ ] Doc de décision
- ⚠️ Conditionne C1-SwordMoveset, C1-BowPOC, C5-ForgeSystem, C5-TalentTree

### C1-SwordMoveset — Moveset épée complet
- [ ] Combo 3 coups légers, finisseur, coup chargé (heavy)
- [ ] RotateTowardLockTarget câblé avec lock-on
- [ ] Épée Mana placeholder
- ⚠️ Nécessite C1-WeaponArchitecture

### C1-SaveDesign — Session design respawn & sauvegarde
- [ ] Modèle respawn, ce qui est sauvegardé, granularité
- [ ] Livrable : spec SaveGame.md

### C1-BowPOC — Arc POC
- [ ] Munitions illimitées, visée, projectile
- ⚠️ Nécessite C1-WeaponArchitecture

### C1-WeaponSwitching — Switching d'armes en combat
- [ ] Via radial, conservation ou reset combo ?

### C1-SFXCombat — Sons de combat de base
- [ ] Attaques, esquive, dégâts, mort, sons UI
- Peut démarrer maintenant

### C1-AnimationsPass1 — Premier pass animations (fin de Couche 1)
- [ ] Strafe gauche/droite distincts
- [ ] Roll sans Root Motion en lock-on
- [ ] Rename ABP_Manny_Platforming -> ABP_Hero

---

## COUCHE 2 — Combat & Ennemis

### C2-SaveGame / C2-EnemyMesh / C2-EnemyAI / C2-EnemyTypes / C2-Boss1

Note : WeaponClass sur BP_Enemy_Base sera supprimée dans C2-EnemyMesh (décision 23/05).
La magie ennemie partagera DT_Spells du hero -- architecture à définir en C2 avec C1-MagicProgressionDesign.

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
| Progression magies : linéaire (puissance/durée) ou arbre de talent ? | C1-MagicProgressionDesign |
| Magie ennemie : DT_Spells partagé ou sous-ensemble dédié ? | C1-MagicProgressionDesign / C2 |
| Distribution future : Steam / itch.io / perso | C8-Build2 |

---

## Historique

- Création : 11/05/2026
- Refonte complète : 14/05/2026
- Resynchro complète : 18/05/2026
- MAJ 21/05/2026 : C1-HitFlashEnemies abandonné, C1-RadialMagie ajouté, C1-InputsUI priorisé
- MAJ 23/05/2026 : C1-InputsUI VALIDE PIE, C1-RadialMagie prochain, ordre jalons révisé
- MAJ 23/05/2026 : décisions C1-RadialMagie actées, C1-MagicProgressionDesign ajouté, SelectedIndex en C1-CleanupDettes
