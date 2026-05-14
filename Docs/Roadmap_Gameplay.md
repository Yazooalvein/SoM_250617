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
| Lock-On | ⚠️ À revoir | Logique + UI à revoir (J-lock) |
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
J-TestBed (mini zone + mini mob + SFX placeholder)
  └─> J-SFX1 (sons de base — remonté en C1 pour calibrer le feel)
        └─> J-lock
              └─> J-Camera
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

### J-TestBed — Zone & Mob de Test (PREMIER JALON)
- [ ] **Mini zone BSP** (1-2h de travail, pas une vraie map) :
  - Couloir avec angle (test caméra espace contraint)
  - Plateforme haute (test caméra verticalité)
  - Obstacle bloquant la vue (test collision caméra)
  - Espace ouvert pour le combat
- [ ] **BP_Enemy_TestBed** (hérite BP_EnemyBase) :
  - Tourne autour du joueur (test lock-on sur cible mobile latéralement)
  - Recule après avoir attaqué (test caméra sur cible qui s'éloigne)
  - Attaque chargée avec tell visuel (test hitstop + screen shake)
  - Mort propre (test feedback mort)
  - BT simple : 3 états (Rôder, Attaquer, Reculer)
- [ ] **SFX placeholder** libres de droits importés (attaque, esquive, impact, mort)
- ⚠️ Objectif : avoir de la matière concrète pour calibrer J-lock et J-Camera

### J-SFX1 — Sons de Base (remonté en C1)
- [ ] Attaques (léger, lourd, finisseur)
- [ ] Esquive, dash, roulade
- [ ] Dégâts reçus, mort joueur
- [ ] Dégâts ennemis, mort ennemi
- [ ] Sons UI : radial menu, quickslot, validation
- ⚠️ Fait avant J-lock pour calibrer le feel du combat sans biais

### J-lock — Révision Lock-On
- [ ] Audit complet système existant
- [ ] Fix détection nouvelles cibles dans le radius (sans reset manuel)
- [ ] Fix z-order indicateur lock (derrière le héros)
- [ ] Fix positionnement barres HP ennemis
- [ ] Comportement caméra pendant Lock-On (lié à J-Camera)
- [ ] Décision : migrer / refactoriser / refaire from scratch ?
- ⚠️ Nécessite J-TestBed pour tester sur un mob qui bouge réellement

### J-Camera — Caméra & Feel de base
- [ ] Révision caméra 3/4 (distance, angle, lag)
- [ ] Collision caméra (pas de clip dans les murs)
- [ ] Caméra Lock-On (smooth tracking cible)
- [ ] Premier pass screen shake (hits reçus, dash)
- [ ] Hitstop POC (freeze frame 2-3 frames sur coup fort)
- [ ] Vibration gamepad standard (hits, mort) — pas de haptique avancé
- ⚠️ Nécessite J-TestBed (obstacles, hauteurs) + J-lock fonctionnel

### J-C — IMC_UI dédié
- [ ] Créer IMC_UI séparé pour inputs menus
- [ ] Migrer : IA_UI_Radial_Cancel, IA_validate_radial_selection, IA_UI_RadialMenu_ChangeCat
- [ ] Nettoyer IMC_Prototype (inputs gameplay uniquement)

### J-15 — Audit Combat Armes
- [ ] Audit BP_ComboManagerComponent — extensible ou refonte ?
- [ ] Décision architecture BP_WeaponType_Base
- [ ] Unification DiscoveredWeapons (PC = source de vérité, retirer du Character)

### J-16 — Architecture Armes
- [ ] BP_WeaponType_Base (classe mère abstraite par TYPE)
- [ ] BP_Weapon_Base devient instance d'un type
- [ ] Structure données armes révisée (DT_Weapons)
- [ ] ⚠️ Conditionne J-17/18/19/Forge

### J-17 — POC Épée
- [ ] Moveset complet Épée (combo 3 coups, finisseur, coup chargé)
- [ ] Feedback combat : flash arme, posture — PAS d'UI visible (ACTÉ)
- [ ] Épée Mana placeholder (asset narratif, sera upgradé via forge)

### J-F — SaveGame
- [ ] Système SaveGame complet
- [ ] Stats joueur, armes débloquées, sorts débloqués
- [ ] Progression hub, flags narratifs (dont flag Général)
- [ ] ⚠️ À faire avant J-18 pour ne pas complexifier le save après

### J-18 — Arc POC
- [ ] Munitions illimitées (ACTÉ)
- [ ] Système de visée (lock-on oriente la flèche, visée libre sans lock)
- [ ] Projectile BP, charge optionnelle

### J-19 — Weapon Switching
- [ ] Switching en combat via radial menu
- [ ] Conservation ou reset combo au switch ? (point ouvert)
- [ ] Transition animations entre types d'armes

### J-B — Animations
- [ ] Consolidation animations en double
- [ ] Animations de transition (idle → combat, switch arme)
- [ ] Animations compagnons (base)

### J-E — Hit Flash Ennemis
- [ ] DMI au BeginPlay sur tous les ennemis
- [ ] M_Enemy_Base avec HitFlashAmount
- [ ] Intégration sur BP_EnemyBase

---

## COUCHE 2 — Combat & Ennemis

### J-EnemyArt — Mesh Ennemis POC
- [ ] Workflow Meshy/AccuRIG pour ennemis (même pipeline que héros)
- [ ] Knight ennemi jouable avec vrai mesh (BP_Enemy_Knight finalisé)
- [ ] Material ennemi + Hit Flash
- [ ] Au moins 2 types visuels distincts (soldat, mage ou archer)

### J-EnemyAI — Révision IA Ennemie
- [ ] Révision comportements (aggro, patrouille, désengagement)
- [ ] IA par type d'arme (épée vs archer vs mage = comportements différents)
- [ ] Hitbox précises par type d'attaque
- [ ] BTService_CheckAggroDistance : révision radius + conditions

### J-EnemyTypes — Nouveaux Types Ennemis
- [ ] Archer (attaque à distance, esquive si corps à corps)
- [ ] Mage (sorts élémentaires, vulnérable en close)
- [ ] Colosse (lent, attaques lourdes, absorbe les combos)
- [ ] Chaque type = BP_Enemy_[Type] héritant BP_EnemyBase

### J-Boss1 — Premier Boss POC
- [ ] Boss Acte 1 (à définir narrativement)
- [ ] Phases de combat (2 minimum)
- [ ] Attaques spéciales + tells visuels
- [ ] Caméra boss dédiée (J-CameraBoss)
- [ ] Musique boss dédiée (lié à J-MUS)

---

## COUCHE 3 — Monde & Navigation

### J-MAP-1 — Map de Test Réelle (apprentissage)
- [ ] Créer une vraie map de terrain (pas LevelPrototyping)
- [ ] Apprendre : Landscape, foliage, lighting, collisions
- [ ] Assez grande pour tester gameplay en situation réelle
- [ ] Zone forêt ou ruines (cohérent avec le lore — monde brisé)
- [ ] Pas de finition artistique — fonctionnelle et lisible

### J-MAP-2 — Ville de l'Oracle (Hub Acte 1)
- [ ] Layout de base du hub (zones : place centrale, forge, sanctuaire, entrée)
- [ ] Éclairage et ambiance (ville partiellement reconstruite)
- [ ] Collision et navigation IA correctes
- [ ] Points d'ancrage pour PNJ (liés à J-Hub1)

### J-MAP-3 — Ville Détruite du Héros (zone de départ)
- [ ] Zone linéaire courte (tutoriel naturel)
- [ ] Ruines, survivants, ambiance post-guerre
- [ ] Premier contact avec un ennemi in-game

### J-Flammy — Système de Voyage Rapide
- [ ] BP_Flammy : asset narratif + mécanique de voyage
- [ ] Points de voyage débloqués progressivement (jalons narratifs)
- [ ] Transition de zone (fondu + chargement)
- [ ] Flammy comme personnage à part entière (réactions, dialogues courts)

### J-Transition — Transitions Entre Zones
- [ ] Système de chargement entre niveaux
- [ ] Loading screen avec illustration (lié à J-LoadingScreen)
- [ ] Persistance état joueur entre zones (lié à J-F)

---

## COUCHE 4 — Systèmes Narratifs & Progression

### J-Dialogue — Système de Dialogues
- [ ] DT_Dialogues (structure : speaker, texte FR/EN, portrait, conditions)
- [ ] Widget dialogue (boîte de texte, portrait, avance au bouton)
- [ ] Déclencheurs : overlap zone, interaction PNJ, jalons narratifs
- [ ] Support localisation dès le départ (StringTable FR + EN)
- [ ] Pas de voix — texte uniquement

### J-Tuto — Tutoriel In-Game
- [ ] Hints contextuels dans les premiers instants du jeu uniquement
- [ ] Déclenchés par situation (premier ennemi vu = hint combat)
- [ ] Affichage minimaliste, pas d'écran dédié
- [ ] Disparaissent après X secondes ou après l'action effectuée
- [ ] Désactivables dans les options

### J-Deités — Toutes les Déités (session groupée)
- [ ] Lumina : sorts déjà faits → intégration narrative complète
- [ ] Luna : sorts + recrutement compagnon (lié à J-Compagnons)
- [ ] Ombre : sorts du héros (type à définir)
- [ ] Sylphide : sorts vent
- [ ] Gnome : sorts terre
- [ ] Salamandre : sorts feu
- [ ] Athanor : sorts forge/feu sacré
- [ ] Ondine : sorts eau (cas spécial — fusion avec la sœur)
- [ ] Dryade : sorts nature (cas spécial — Oracle)
- [ ] Chaque déité = bloc de 4 sorts (attaque, buff, soin, ultime)
- [ ] ⚠️ Arbres de talents auront une incidence sur les sorts de chaque déité

### J-Corruption — Système de Corruption Magique
- [ ] BP_CorruptionComponent (0-100)
- [ ] Augmente à chaque sort utilisé (variable selon type)
- [ ] Effets par seuil : 25 / 50 / 75 / 100
- [ ] Indicateur HUD minimal (sans surcharge visuelle)
- [ ] Sanctuaires de purification (liés à J-MAP)
- [ ] Sorts de soin corrompent-ils moins ? (point ouvert)

### J-ChoixMoral — Flag Général de l'Empire
- [ ] Variable de flag persistante dans SaveGame : bGeneralSpared (bool)
- [ ] Séquence confrontation Général (fin Acte 2)
- [ ] Aucun indicateur de conséquence visible
- [ ] Conséquences Acte 4 : Luna vit ou meurt selon flag
- [ ] Fragment de vérité sur la sœur du héros (si épargné)

### J-Hub1 — Ville de l'Oracle État 1
- [ ] PNJ de base présents (Lumina, Oracle, quelques survivants)
- [ ] Dialogues déclenchables
- [ ] État : ville quasi-vide, premiers bâtiments debout

### J-Hub2 — Ville de l'Oracle État 2
- [ ] Forgeron nain installé (forge accessible)
- [ ] Nouveaux PNJ arrivés (liés à progression narrative)
- [ ] Variable HubProgressionLevel dans GameInstance

### J-Hub3 — Ville de l'Oracle État 3
- [ ] Reconstruction avancée (visuellement différent de l'état 1)
- [ ] Shop basique, quêtes secondaires disponibles
- [ ] Flammy présent comme point de voyage

### J-Compagnons1 — Luna (PNJ combattante)
- [ ] BP_AIController_Companion_Base
- [ ] Luna : comportement combat, formation
- [ ] Action via L2 (mapping PS5)
- [ ] Lien avec J-ChoixMoral (survie conditionnelle)

### J-Compagnons2 — Lumina (PNJ non combattante)
- [ ] Lumina : soins, guidance narrative
- [ ] Action via R2 (mapping PS5)
- [ ] Présente mais ne combat pas

### J-Compagnons3 — Garçon Loup & Colosse
- [ ] Recrutement dans la région volcanique (narratif)
- [ ] Comportements combat distincts (loup = rapide, colosse = lent/lourd)

### J-Quetes — Système de Quêtes
- [ ] DT_Quests (structure : ID, titre FR/EN, objectifs, récompenses, conditions)
- [ ] BP_QuestManager dans GameInstance
- [ ] Quêtes principales (Acte 1) + quelques quêtes secondaires
- [ ] Suivi dans menu pause (pas d'UI en jeu surchargée)

### J-Lore — Codex Lore Débloquable
- [ ] DT_Lore (entrées débloquées via exploration ou dialogues PNJ)
- [ ] Widget codex dans menu pause
- [ ] Contenu : personnages, déités, lieux, histoire

### J-SœurReveal — Révélation Narrative Sœur du Héros
- [ ] Séquence Acte 3 : héros retrouve sa sœur / Ondine
- [ ] Mort de l'Oracle (événement pivot)
- [ ] Cinématique légère via Sequencer UE5
- [ ] Divergence selon flag Général

---

## COUCHE 5 — Forge & Équipement

### J-Forge1 — BP_ForgeComponent POC
- [ ] Interface forge (liste armes upgradables, matériaux requis)
- [ ] NPC Athanor (forgeron nain) comme point d'accès
- [ ] Matériaux liés au lore Mana (graines ? symboles ?) — point ouvert

### J-Forge2 — Évolution Armes
- [ ] Épée → Flamberge → Katana
- [ ] Arc court → Arc long → Arbalète → Arc elfique
- [ ] Jalons narratifs comme conditions de déblocage (pas juste de l'or)

### J-Equipement — Système d'Équipement
- [ ] Bonus % sur stats (pas de stats plates)
- [ ] Intégré au système SetStatValue existant
- [ ] Affiché dans menu pause

### J-Talent — Arbre de Talent par Type d'Arme
- [ ] Un arbre par type d'arme (Épée, Arc, etc.)
- [ ] Incidence possible sur les sorts de déités associées
- [ ] Structure DT_Talents + BP_TalentManager

---

## COUCHE 6 — Audio & Feedback

*Note : J-SFX1 a été remonté en Couche 1 (avant J-lock) pour calibrer le feel dès le début.*

### J-SFX2 — Ambiances Par Zone
- [ ] Ambiance forêt / ruines (vent, insectes, décombres)
- [ ] Ambiance volcanique
- [ ] Ambiance hub (ville qui reprend vie)

### J-SFX3 — Sons de Magie
- [ ] Son par type de sort (feu, lumière, eau, terre...)
- [ ] Son de corruption (ambiant, augmente avec le niveau)

### J-MUS-1 — Thème Principal + Combat
- [ ] Workflow : fredonnement → Suno → export MP3 → UE5
- [ ] Prompt établi : dark orchestral, 60 BPM, D minor, cello lead
- [ ] Thème combat : plus rapide, même tonalité

### J-MUS-2 — Ambiances Par Zone
- [ ] Un thème par zone majeure (ville détruite, hub, volcan, neiges...)

### J-MUS-3 — Musique de Boss
- [ ] Boss final Acte 1
- [ ] Boss Démon Mana (Acte 3)
- [ ] Démon Primordial (Acte 4)

### J-AudioMix — Mixage Global
- [ ] Volumes par catégorie (musique, SFX, ambiance, UI)
- [ ] Options dans menu (curseurs volume)
- [ ] Atténuation spatiale correcte (sons 3D vs 2D)

---

## COUCHE 7 — UI/UX Complet

### J-MenuPrincipal — Écran Titre
- [ ] Logo, New Game, Continue, Options, Quitter
- [ ] Illustration ou fond animé
- [ ] Continue grisé si pas de save existant

### J-MenuOptions — Options
- [ ] Volume musique / SFX / ambiance
- [ ] Langue (FR / EN)
- [ ] Remapping touches (gamepad + clavier)
- [ ] Taille du texte (accessibilité)

### J-MenuPause — Menu Pause
- [ ] Stats joueur
- [ ] Équipement actuel
- [ ] Sorts débloqués
- [ ] Quêtes en cours
- [ ] Codex lore
- [ ] Accès options
- [ ] Time Dilation 0 ou pause complète ? (point ouvert)

### J-DeathScreen — Écran de Mort
- [ ] Écran simple (fondu noir, texte)
- [ ] Respawn au dernier sanctuaire (Dark Souls) ou checkpoint classique (Seiken/KH) — point ouvert
- [ ] Pas de pénalité pour l'instant (à décider)

### J-LoadingScreen — Écrans de Chargement
- [ ] Illustration par zone
- [ ] Tip de gameplay (court, contextuel)
- [ ] Barre de progression

### J-HUD-Polish — HUD Final
- [ ] Icônes quickslot avec sorts assignés
- [ ] Indicateur corruption (minimal, pas envahissant)
- [ ] Pas de minimap — boussole légère si nécessaire

### J-Loc — Localisation FR/EN
- [ ] StringTable dès le début (ne pas hardcoder le texte)
- [ ] FR = langue principale, EN = traduction
- [ ] Tous les dialogues, UI, menus, hints

---

## COUCHE 8 — Qualité & Build

### J-Debug — Panneau Debug In-Game
- [ ] Téléportation vers zones
- [ ] Modifier stats à la volée
- [ ] Activer/désactiver flags narratifs
- [ ] Afficher état SaveGame
- [ ] Désactivé en build release

### J-Acte1Test — Map Test Acte 1 Jouable
- [ ] Tous les systèmes fondations actifs ensemble
- [ ] Zone de départ → hub → première zone → premier boss
- [ ] Dialogues, sons, morts, sauvegardes fonctionnels
- [ ] Objectif : session de jeu complète de 30-45 min jouable

### J-Perf1 — Premier Audit Performances
- [ ] Profiling GPU/CPU en jeu
- [ ] Budget DrawCall par zone
- [ ] LODs ennemis et environnement

### J-Perf2 — Optimisation
- [ ] LODs, culling, streaming de niveaux
- [ ] Objectif : 60 FPS stable sur configuration cible

### J-Crash — Chasse aux Crashes
- [ ] Session dédiée edge cases
- [ ] Test mort/respawn en boucle
- [ ] Test switching armes + magie rapide
- [ ] Test sauvegarde corrompue

### J-Build1 — Première Build Packagée
- [ ] Build Windows jouable hors éditeur
- [ ] Installer correctement (icône, nom, version)
- [ ] Test sur machine distincte si possible

### J-Build2 — Verticale Slice Acte 1
- [ ] Build complète Acte 1 (du début au boss de fin d'acte)
- [ ] Suffisamment polie pour être montrée
- [ ] Base pour décision distribution future

---

## Sessions Créatives (intercalées librement)

| Session | Contenu |
|---------|---------|
| J-ART-Hero | LODs + correction 6 doigts + sockets HandGrip affinés |
| J-ART-Enemies | Meshes ennemis (Knight finalisé + 1-2 types supplémentaires) |
| J-ART-Weapons | Assets armes séparés (Sword_01, 2HSword_01, Arc_01...) |
| J-ART-NPC | Lumina, Luna, Athanor placeholders |
| J-MAP-1 | Map de test réelle (apprentissage terrain UE5) |
| J-MAP-2 | Ville de l'Oracle layout |
| J-MAP-3 | Ville détruite du héros |
| J-MUS-1 | Thème principal + combat |
| J-MUS-2 | Ambiances zones |
| J-MUS-3 | Musiques de boss |

---

## Points de Design Encore Ouverts

| Sujet | État |
|-------|------|
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
- Mise à jour : 14/05/2026 — Ajout J-TestBed, J-SFX1 remonté en C1
