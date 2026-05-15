# Roadmap Gameplay — Shadow of Mana

Document de référence pour la planification complète du projet.
Mis à jour après chaque session de design ou de développement.

---

## Modules existants (POC validés)

| Module | État | Notes |
|--------|------|-------|
| Stats (SetStatValue / OnStatChanged) | ✅ Stable | Architecture solide, ne bougera pas |
| HUD event-driven | ✅ Stable | Zero polling, extensible |
| Iframes dash/roll | ✅ Stable | Via AnimNotify, Dark Souls style |
| Mort du joueur | ✅ Stable | bIsDead + OnPlayerDeath dispatcher |
| Lock-On | ⚠️ En cours | J-lock partiel -- strafe OK, dettes mineures restantes |
| Strafe lock-on | ✅ PIE | ABP_Manny_Platforming + BS_Unarmed_Strafe |
| Radial menu unifié | ✅ Stable | J-13 complet + J-Nettoyage propre |
| Quickslot POC | ✅ POC | 3 slots, multi-pages futur |
| Combo system | ✅ POC | TMap + fenêtre dynamique, à évaluer J-15 |
| IA ennemis | ✅ POC | Behavior Tree + PawnSensing |
| Hit Flash joueur | ✅ Stable | M_Hero HitFlashAmount |
| Hit Flash ennemi | ⚠️ Partiel | Nécessite DMI + vrai enemy mesh |
| Système de magie | ✅ POC | BP_MagicComponent + 4 sorts Lumina validés PIE |
| Hero placeholder | ✅ PIE | Mesh Meshy + AccuRIG + retargeting Mannequin |

---

## Vue d'ensemble — Couches de développement

```
COUCHE 1 — Fondations gameplay        (maintenant → court terme)
COUCHE 2 — Combat & Ennemis           (après fondations)
COUCHE 3 — Monde & Navigation         (en parallèle possible avec C2)
COUCHE 4 — Systèmes narratifs         (après monde + combat)
COUCHE 5 — Forge & Équipement         (après systèmes narratifs)
COUCHE 6 — Audio & Feedback           (SFX1 en C1, reste intercalé)
COUCHE 7 — UI/UX complet              (intercalé, avant build)
COUCHE 8 — Qualité & Build            (fin de développement)

Sessions créatives (J-ART / J-MUS / J-MAP) : intercalées librement.
```

---

## Ordre de dépendances global

```
J-lock (fin)
  └─> J-Camera
        └─> J-TestBed (mini zone + mob + SFX placeholder)
              └─> J-SFX1
                    └─> J-15/16/17 (Armes + Combo)
                          └─> J-F (SaveGame)
                                └─> J-18/19 (Arc + Switching)
                                      └─> J-B/E (Animations + Hit Flash)
                                            └─> J-EnemyArt
                                                  └─> J-EnemyAI
                                                        └─> J-Boss1

J-MAP-1 (Map de test réelle, apprendre la compétence)
  └─> J-Dialogue
        └─> J-Hub1/2/3
              └─> J-Deités (toutes ensemble)
                    └─> J-Corruption
                          └─> J-ChoixMoral
                                └─> J-Acte1Test

J-Acte1Test
  └─> J-Perf1
        └─> J-Build1 (première build packagée)
              └─> J-Build2 (verticale slice Acte 1)
```

---

## COUCHE 1 — Fondations gameplay

### J-lock — Révision Lock-On (EN COURS)
**Fait :**
- [x] Fix IsLockOnActive (retournait vide)
- [x] Fix espace dans dispatcher OnLockOnDeactivated
- [x] Bindings OnLockOnActivated/Deactivated dans BP_PlatformingCharacter
- [x] bOrientRotationToMovement + UseControllerRotationYaw corrects
- [x] Strafe fonctionnel PIE (ABP_Manny_Platforming + BS_Unarmed_Strafe)
- [x] Indicateur lock : SetVisibility selon frustum (Project World to Screen bool)

**Reste à faire :**
- [ ] Unification cooldown switch (doublon PC/Component)
- [ ] Tests edge cases (mort ennemi, switch cible, délock)
- [ ] Fix TargetActor espace dans UI_LockOnIndicator

**Notes design lock-on pour J-Camera :**
- Caméra KH style : suit activement pour garder la cible lockée visible
- Délock automatique si cible hors champ (couloir, hauteur) -- DS style
- Marqueur à repenser : cercle au sol / flèche / autre image (pas juste LockOnCross)
- À brainstormer avant J-Camera

### J-Camera — Caméra & Feel de base
- [ ] Révision caméra 3/4 (distance, angle, lag)
- [ ] Collision caméra (pas de clip dans les murs)
- [ ] Caméra Lock-On KH style (suit pour garder cible visible)
- [ ] Délock automatique si cible hors champ (DS style)
- [ ] Nouveau marqueur lock-on (cercle au sol ? flèche ? à décider)
- [ ] Premier pass screen shake (hits reçus, dash)
- [ ] Hitstop POC (freeze frame 2-3 frames sur coup fort)
- [ ] Vibration gamepad standard (hits, mort) — pas de haptique avancé
- ⚠️ Nécessite J-lock terminé + J-TestBed pour matière de test

### J-TestBed — Zone & Mob de Test
- [ ] Mini zone BSP : couloir, plateforme, obstacle, espace ouvert
- [ ] BP_Enemy_TestBed (hérite BP_EnemyBase) : tourne, recule, attaque chargée
- [ ] SFX placeholder libres de droits importés

### J-SFX1 — Sons de Base (remonté en C1)
- [ ] Attaques, esquive, dash, dégâts, mort (joueur + ennemi)
- [ ] Sons UI : radial menu, quickslot, validation

### J-C — IMC_UI dédié
- [ ] Créer IMC_UI séparé pour inputs menus
- [ ] Migrer : IA_UI_Radial_Cancel, IA_validate_radial_selection, IA_UI_RadialMenu_ChangeCat
- [ ] Nettoyer IMC_Prototype (inputs gameplay uniquement)

### J-15 — Audit Combat Armes
- [ ] Audit BP_ComboManagerComponent (architecture TMap confirmée solide -- a priori à conserver)
- [ ] Décision architecture BP_WeaponType_Base
- [ ] Unification DiscoveredWeapons (PC = source de vérité, retirer du Character)

### J-16 — Architecture Armes
- [ ] BP_WeaponType_Base (classe mère abstraite par TYPE)
- [ ] BP_Weapon_Base devient instance d'un type
- [ ] Structure données armes révisée (DT_Weapons)
- [ ] ⚠️ Conditionne J-17/18/19/Forge

### J-17 — POC Épée
- [ ] Moveset complet Épée (combo 3 coups, finisseur, coup chargé)
- [ ] RotateTowardLockTarget du ComboManager à vérifier/câbler avec nouveau lock-on
- [ ] Feedback combat : flash arme, posture — PAS d'UI visible (ACTÉ)
- [ ] Épée Mana placeholder (asset narratif, sera upgradé via forge)

### J-F — SaveGame
- [ ] Système SaveGame complet
- [ ] Stats joueur, armes débloquées, sorts débloqués
- [ ] Progression hub, flags narratifs (dont flag Général)

### J-18 — Arc POC
- [ ] Munitions illimitées (ACTÉ)
- [ ] Système de visée (lock-on oriente la flèche, visée libre sans lock)
- [ ] Projectile BP, charge optionnelle

### J-19 — Weapon Switching
- [ ] Switching en combat via radial menu
- [ ] Conservation ou reset combo au switch ? (point ouvert)
- [ ] Transition animations entre types d'armes

### J-B — Animations
- [ ] Animations strafe gauche/droite distinctes (placeholder actuel = Jog_Left x2)
- [ ] Consolidation animations en double
- [ ] Animations de transition (idle → combat, switch arme)

### J-E — Hit Flash Ennemis
- [ ] DMI au BeginPlay sur tous les ennemis
- [ ] M_Enemy_Base avec HitFlashAmount
- [ ] Intégration sur BP_EnemyBase

---

## COUCHE 2 — Combat & Ennemis

### J-EnemyArt — Mesh Ennemis POC
- [ ] Workflow Meshy/AccuRIG pour ennemis (même pipeline que héros)
- [ ] Knight ennemi jouable avec vrai mesh (BP_Enemy_Knight finalisé)
- [ ] WeaponClass dans BP_EnemyBase à rendre générique (hardcodé sur BP_Enemy_Sword01)
- [ ] Material ennemi + Hit Flash
- [ ] Au moins 2 types visuels distincts

### J-EnemyAI — Révision IA Ennemie
- [ ] Révision comportements (aggro, patrouille, désengagement)
- [ ] IA par type d'arme (épée vs archer vs mage)
- [ ] Hitbox précises par type d'attaque
- [ ] BTService_CheckAggroDistance : révision radius + conditions

### J-EnemyTypes — Nouveaux Types Ennemis
- [ ] Archer, Mage, Colosse — chacun héritant BP_EnemyBase

### J-Boss1 — Premier Boss POC
- [ ] Boss Acte 1, 2 phases, attaques spéciales + tells visuels
- [ ] Caméra boss dédiée, musique boss dédiée

---

## COUCHE 3 — Monde & Navigation

### J-MAP-1 — Map de Test Réelle (apprentissage)
- [ ] Landscape, foliage, lighting, collisions
- [ ] Zone forêt ou ruines, pas de finition artistique

### J-MAP-2 — Ville de l'Oracle (Hub Acte 1)
- [ ] Layout de base, éclairage, navigation IA, points PNJ

### J-MAP-3 — Ville Détruite du Héros (zone de départ)
- [ ] Zone linéaire courte, tutoriel naturel

### J-Flammy — Système de Voyage Rapide
- [ ] BP_Flammy, points débloqués progressivement, dialogues courts

### J-Transition — Transitions Entre Zones
- [ ] Chargement entre niveaux, persistance état joueur

---

## COUCHE 4 — Systèmes Narratifs & Progression

### J-Dialogue — Système de Dialogues
- [ ] DT_Dialogues (FR/EN), widget dialogue, déclencheurs, StringTable

### J-Tuto — Tutoriel In-Game
- [ ] Hints contextuels minimalistes, premiers instants uniquement, désactivables

### J-Deités — Toutes les Déités (session groupée)
- [ ] Lumina (faits) → intégration narrative
- [ ] Luna, Ombre, Sylphide, Gnome, Salamandre, Athanor, Ondine, Dryade
- [ ] Chaque déité = 4 sorts (attaque, buff, soin, ultime)
- [ ] Arbres de talents auront une incidence sur les sorts

### J-Corruption — Système de Corruption Magique
- [ ] BP_CorruptionComponent (0-100), effets par seuil 25/50/75/100
- [ ] Indicateur HUD minimal, sanctuaires de purification

### J-ChoixMoral — Flag Général de l'Empire
- [ ] bGeneralSpared dans SaveGame, conséquences Acte 4

### J-Hub1/2/3 — Ville de l'Oracle États 1-2-3
- [ ] PNJ, dialogues, forge, HubProgressionLevel, Flammy

### J-Compagnons1/2/3 — Luna, Lumina, Loup & Colosse

### J-Quetes — Système de Quêtes
- [ ] DT_Quests, BP_QuestManager, suivi dans menu pause

### J-Lore — Codex Lore Débloquable
- [ ] DT_Lore, widget codex dans menu pause

### J-SœurReveal — Révélation Narrative
- [ ] Séquence Acte 3, Sequencer UE5, divergence selon flag

---

## COUCHE 5 — Forge & Équipement

### J-Forge1/2 — BP_ForgeComponent + Évolution Armes
- [ ] Interface forge, NPC Athanor, conditions narratives de déblocage
- [ ] Épée → Flamberge → Katana, Arc → Arc long → Arbalète → Arc elfique

### J-Equipement — Système d'Équipement
- [ ] Bonus % stats, intégré SetStatValue, affiché menu pause

### J-Talent — Arbre de Talent par Type d'Arme
- [ ] DT_Talents + BP_TalentManager, incidence sur sorts déités

---

## COUCHE 6 — Audio & Feedback

*J-SFX1 remonté en Couche 1.*

### J-SFX2 — Ambiances Par Zone
### J-SFX3 — Sons de Magie
### J-MUS-1/2/3 — Thèmes musicaux
### J-AudioMix — Mixage Global

---

## COUCHE 7 — UI/UX Complet

### J-MenuPrincipal / J-MenuOptions / J-MenuPause / J-DeathScreen / J-LoadingScreen
### J-HUD-Polish — Icônes quickslot, indicateur corruption, boussole légère
### J-Loc — Localisation FR/EN (StringTable, pas de hardcode)

---

## COUCHE 8 — Qualité & Build

### J-Debug — Panneau debug in-game (désactivé en release)
### J-Acte1Test — Map test Acte 1 jouable (30-45 min de jeu)
### J-Perf1/2 — Profiling + Optimisation (cible 60 FPS)
### J-Crash — Session edge cases
### J-Build1/2 — Build packagée Windows + Verticale Slice Acte 1

---

## Sessions Créatives (intercalées librement)

| Session | Contenu |
|---------|---------|
| J-ART-Hero | LODs + correction 6 doigts + sockets affinés |
| J-ART-Enemies | Meshes ennemis (Knight + 1-2 types) |
| J-ART-Weapons | Assets armes séparés (Sword_01, 2HSword_01, Arc_01...) |
| J-ART-NPC | Lumina, Luna, Athanor placeholders |
| J-MAP-1/2/3 | Maps terrain UE5 |
| J-MUS-1/2/3 | Thèmes musicaux |

---

## Points de Design Encore Ouverts

| Sujet | État |
|-------|------|
| Marqueur lock-on : cercle au sol / flèche / autre | Ouvert (à décider avant J-Camera) |
| Forge : matériaux exacts (graines Mana ?) | Ouvert |
| Switching armes : reset combo ou conservation ? | Ouvert |
| Corruption : les sorts de soin corrompent-ils moins ? | Ouvert |
| Compagnons : mort permanente possible hors choix moral ? | Ouvert |
| Garçon Loup : Salamandre ou Gnome ? | Ouvert |
| Colosse : Gnome confirmé ? | Ouvert |
| Flammy : quel jalon narratif débloque le voyage rapide ? | Ouvert |
| Touchpad PS5 : carte, journal, ou autre ? | Ouvert |
| Menu pause : Time Dilation 0 ou pause complète ? | Ouvert |
| Death screen : respawn sanctuaire (DS) ou checkpoint (Seiken/KH) ? | Ouvert |
| Quickslot switch : press = utiliser, hold = changer de page ? | Ouvert |
| Distribution future : Steam / itch.io / perso | Ouvert |

---

## Historique

- Création : 11/05/2026
- Refonte complète : 14/05/2026
- Mise à jour : 15/05/2026 — J-lock partiel coché, notes J-Camera lock-on, ordre dépendances révisé
