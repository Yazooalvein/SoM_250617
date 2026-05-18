# Journal des Modifications -- Shadow of Mana

## Objectif
Suivi precis de toutes les evolutions majeures du projet.

## Entrees

### 17/06/2025 -- Nico -- Creation du projet
- Initialisation SoM sous UE5.6, template Third Person Platforming

### 18/06/2025 -- Nico
- Refactoring pipeline Gameplay de base (Dash, Roll, Jump, Stamina)

### 19-20/06/2025 -- Nico
- Lock-On, Menu Radial, refonte Combo

### 21/06/2025 -- Nico
- Refactorisation BP_ComboManagerComponent (TMap, fenetre dynamique)

### 24/06/2025 -- Nico
- Systeme armes data-driven, Menu Radial data-driven, Combo multi-armes

### 26/06/2025 -- Nico
- BPI_TakeDamage, BP_Enemy_Base ReceiveDamage + OnDeath

### 27/06/2025 -- Nico
- BP_AIController_Enemy_Base, PawnSensing, aggro/perte

### 20/07/2025 -- Nico
- Animation Weapon Integration

### 07/05/2026 -- Jalons #1 a #7
- #1 : MCP + Hit Flash joueur (M_Hero HitFlashAmount)
- #2 : Mort du joueur (bIsDead, OnPlayerDeath, LoseAggro)
- #3 : OnStatChanged dispatcher (SetStatValue = unique point)
- #4 : Unification inputs (source unique InputActions/)
- #5 : Iframes dash/roll (bIsInvincible via AnimNotify)
- #6 : UI event-driven (zero polling, OnStatChanged)
- #7 : Hit Flash ennemi partiel + fix GameMode PlayerController

### 11/05/2026 -- Jalon #8 -- Migration UE5.7 + UnrealClaude
- Projet migre UE5.6 -> UE5.7.4
- UnrealClaude v1.4.5 : 28 outils MCP, panel operationnel
- Workflow dual-agent mis en place (Docs/Session_UnrealClaude.md)

### 11/05/2026 -- Jalon #9 -- Audit complet + nettoyage
- Fixes config (DefaultGame.ini, uproject, ProjectName)
- Nettoyage : ThirdPerson/, IA debug, Lvl_Platforming GameMode Override

### 11/05/2026 -- Session design
- Lore : Docs/Lore_ShadowOfMana.md
- Roadmap : Docs/Roadmap_Gameplay.md
- Architecture magie : Docs/Architecture/Magic_System.md

### 12/05/2026 -- Jalons J-10 a J-14 -- POC Systeme Magie VALIDE

#### Structure assets (Content/Systems/Magic/)
- BP_MagicComponent, BP_SpellBase
- E_SpellCategory, E_SpellTarget, E_DeliveryType, FSoM_SpellData, FSoM_DeitySpells, DT_Spells
- BP_Spell_Heal, BP_Spell_Attack, BP_Spell_Buff, BP_Spell_Debuff (Lumina) -- VALIDES PIE

#### BP_MagicComponent
- UnlockedSpells, QuickslotSlots, SpellCooldowns, bIsCasting
- CastSpell : Switch E_SpellTarget -> SpawnActor -> Execute -> ConsumeMana -> cooldown

### 12/05/2026 -- Jalon J-15 -- UI_HUD_Main FINALISE
- SizeBox_Weapon (64x64) + HUD_Main_VertBox (HP/ST/MP/XP)
- RichTextBlock HP/ST/MP + UpdateStatText + DT_HUD_RichTextStyle

### 12-13/05/2026 -- Jalon J-13 COMPLET -- Radial Menu + Quickslot

#### Radial Menu (UI_Radial_Main) -- VALIDE PIE
- Navigation par cran (stick G/D), lerp fluide, wrap correct
- Fix drift (RadialContainer 0.01x0.01), fix sens rotation
- PopulateWeaponSlots, SwitchCategory, ValidateSelectedWeapon -- VALIDES PIE

#### Quickslot POC -- VALIDE PIE
- 3 variables dans PC : QuickslotUp/Left/Right (FName, SpellID)
- IA_Quickslot_Up/Left/Right -> CastSpell via MagicComponent

---

### 14/05/2026 -- Session creative J-MUS (exploration workflow)
- Workflow : Fredonnement -> Suno (gratuit 50 credits/jour) -> Export MP3 -> UE5
- Prompt theme overworld sombre etabli (60 BPM, D minor, cello lead)

---

### 14/05/2026 -- Session creative J-ART ; Hero PLACEHOLDER COMPLET
- Workflow valide : Dessin -> Leonardo.ai -> Gemini -> Meshy 5 -> AccuRIG -> UE5.7
- Design palette actee, retargeting VALIDE PIE (ABP_Manny reutilise via Compatible Skeletons)
- Dettes : 6 doigts, retopo 246K -> 10-15K, LODs, sockets HandGrip a affiner

---

### 14/05/2026 -- J-Nettoyage COMPLET
- BP_SoM_HeroCharacter : WeaponDataTest supprimee
- BP_SoM_PlayerController : RadialMenuRef, SlotRowNames, SlotIcons supprimes
- Assets : UI_RadialMenu, UI_RadialSlot_old, BP_PlatformingGameMode, BP_test_IA
- Reorganisation dossier Enemies (Animations/, Model/, Blueprints/)

---

### 14/05/2026 -- Session design -- Roadmap globale refondee
- ~50 jalons, 8 couches, projet complet de A a Z
- Decisions : FR+EN, tuto minimaliste, vibration standard
- Ordre revise : J-lock -> J-Camera -> J-TestBed -> J-15/16/17

---

### 15/05/2026 -- J-lock COMPLET -- VALIDE PIE

#### Fixes BP_CombatLockOnComponent
- Fix `IsLockOnActive` : retourne desormais `bisLockOnActive` (etait vide)
- Fix espace dans dispatcher : `OnLockOnDeactivated ` -> `OnLockOnDeactivated`

#### Fixes BP_SoM_PlayerController
- Fix bind dispatcher : "On Lock on Activated/Deactivated" (custom) et non "On Component Activated"
- UpdateLockOnUIIndicator : SetVisibility selon Project World to Screen bool
- Socket indicateur lock-on deplace au-dessus de la tete (nouveau socket sur skeleton Mannequin)

#### Fixes BP_SoM_HeroCharacter
- Bindings OnLockOnActivated/Deactivated au BeginPlay :
  - Activated : bOrientRotationToMovement=false + UseControllerRotationYaw=true
  - Deactivated : bOrientRotationToMovement=true + UseControllerRotationYaw=false

#### ABP_Manny_Platforming -- Strafe VALIDE PIE
- Variables : Strafe (float via DotProduct), Can Strafe (bool NOT bOrientRTM)
- State Machine : etat LockedOn_Strafe + transitions Idle/Walk <-> LockedOn_Strafe
- BS_Unarmed_Strafe : Content/Characters/Mannequins/Anims/Unarmed/ (Forward x Strafe [-1,1])
- Animations placeholder : MF_Unarmed_Jog_Left pour gauche ET droite -- a affiner en J-B

#### Tests edge cases VALIDES PIE
- Mort ennemi : delock/switch automatique
- Switch cible (stick droit) : fonctionnel
- Delock manuel (R3) : retour locomotion normale
- Delock hors range
- Indicateur positionne au-dessus de la tete
- Indicateur masque si hors frustum

---

### 15/05/2026 -- J-Renommage COMPLET

#### Convention de nommage unifiee
- `BP_PlatformingCharacter` -> `BP_SoM_HeroCharacter`
- `BP_PlatformingPlayerController` -> `BP_SoM_PlayerController`
- `BP_EnemyBase` -> `BP_Enemy_Base`
- `BB_enemy` -> `BB_Enemy_Base`
- `BT_Enemy` -> `BT_Enemy_Base`
- `BP_enemyTest` -> `BP_Enemy_Test`
- `Datatable_FCombo` -> `DT_Combo_Base`
- `Datatable_StatList` -> `DT_StatList`
- Renames effectues via UE Rename + Fix Up Redirectors, VALIDE PIE
- `ABP_Manny_Platforming` -> rename prevu en `ABP_Hero` lors de J-B (chantier animations)

---

### 17/05/2026 -- J-Camera COMPLET -- VALIDE PIE

#### Fixes permanents
- `BP_SoM_PlayerController` On Possess : SET PlayerCharacterRef (Cast Possessed Pawn -> BP_SoM_HeroCharacter)
  - Bug : PlayerCharacterRef etait None -> erreurs runtime au Tick
- Tick PC : guard NOT Is Dashing / NOT Is Rolling dans AND condition UpdateLockOnRotation

#### SpringArm ajuste (BP_SoM_HeroCharacter)
- Target Arm Length : 400 -> 350
- Socket Offset Z : 0 -> 60
- Camera Lag Speed : 16 -> 8
- Camera Lag Max Distance : 0 -> 200

#### Screen Shake -- VALIDE PIE (debloque par V2)
- CS_HitReceived (Content/Systems/Camera/) : PerlinNoise, Pitch 1.5, Roll 1.0, Freq 20, Duration 0.3
- CS_EnemyDeath (Content/Systems/Camera/) : PerlinNoise, Pitch 3.0, Yaw 0.5, Roll 2.0, Freq 15, Duration 0.4
- BP_SoM_HeroCharacter ReceiveDamage : Client Start Camera Shake (CS_HitReceived) apres HitFlash
- BP_Enemy_Base KillMeNow : Client Start Camera Shake (CS_EnemyDeath) avant Destroy

#### IA_Look deplace dans BP_SoM_PlayerController
- Fonction `Aim` creee dans le PC (Axis X, Axis Y)
- IA_Look retire de BP_SoM_HeroCharacter
- VALIDE PIE

#### UpdateLockOnRotation V2 -- VALIDE PIE
- Logique conditionnelle remplace SetControlRotation systematique
- RInterpTo InterpSpeed branche sur LockOnReturnSpeed (3.0)

---

### 18/05/2026 -- J-LockMove COMPLET (partiel) -- VALIDE PIE

#### Fixes BP_SoM_HeroCharacter -- fonction Move()
- Probleme : En lock-on, dash et roll partaient vers l'ennemi au lieu de suivre le stick
- Cause : Move() utilisait GetControlRotation -> GetForwardVector/GetRightVector
  En lock-on, Control Rotation pointe vers l'ennemi
- Solution : Branch(bisLockOnActive) dans Move() :
  - Lock-on actif : GetPlayerCameraManager -> GetCameraRotation -> Yaw seulement -> MakeRotator(0,yaw,0) -> GetForward/RightVector
  - Hors lock-on : comportement original (GetControlRotation)
- Variables additionnelles : LastAxisX, LastAxisY (stockees au Triggered de IA_Move)
- Deplacement en lock-on VALIDE PIE (direction stick correcte)
- Camera retient vers l'ennemi apres delai VALIDE PIE
- Rotation Rate -1 dans CharacterMovement : pivot instantane hors lock-on

#### Dette J-LockMove2 -- reportee
- Probleme : En lock-on, le roll part toujours vers l'ennemi
- Cause racine : Root Motion en World Space -- elle suit l'orientation du character
  au moment du lancement du montage, et UseControllerRotationYaw=true
  force le character a regarder l'ennemi chaque frame
- Piste : Passer le Roll en approche sans Root Motion :
  LaunchCharacter dans la direction stick camera + animation visuelle seulement
  (architecture DS/KH propre)
- A traiter en J-B lors du chantier animations

---

### 18/05/2026 -- J-TestBed COMPLET -- VALIDE PIE

#### Map Lvl_TestBed (Content/Maps/)
- Sol BSP checker 4000x4000, mur BSP, plateforme sureleve
- Cubes StaticMesh x4 pour obstacles pathfinding IA
- NavMeshBoundsVolume couvrant toute la zone (P -> vert valide)
- Lighting Movable : DirectionalLight + SkyLight + SkyAtmosphere (zero bake)
- GameMode Override : BP_SoM_GameMode
- PlayerStart positionne au centre

#### BP_Enemy_TestBed (Content/Characters/Enemies/Blueprints/)
- Enfant de BP_Enemy_Base
- MaxHealth, CurrentHealth, AttackRadius exposes Instance Editable + categorie Default
- Pas de BT dedie : utilise BP_AIController_Enemy_Base + BT_Enemy_Base par heritage
- Stats tweakables directement dans le Details panel de la map
- Lecon : pas de SetStatValue cote ennemi (contrairement au hero) -- expose les variables natives

#### SFX placeholder (Content/Audio/SFX/Combat/)
- Hit joueur recu : branche sur ReceiveDamage (BP_SoM_HeroCharacter)
- Attaque ennemi : branche sur logique attaque (BP_Enemy_Base)
- Roll hero : branche sur AnimNotify iframes existante
- Branchement direct Play Sound at Location -- pas de SoundCue a ce stade
- Source packs : Free Realistic Sword SFX (Epic Forums) + 50 Free Game Sounds (Fab)

#### Points d'attention
- BT_TestBed et BB_TestBed crees puis abandonnes : inutiles, supprimer du projet
- BP_Enemy_Base n'a pas de SetStatValue : stats directement en variables Float
- OnSeePawn dans BP_Enemy_Base ecrit dans BB_Enemy_Base (pas un BB dedie TestBed)

---

### 18/05/2026 -- J-15 Fix attaque hero -- VALIDE PIE

#### Diagnostic
- Cause racine : `ChoosenWeapon` jamais sette dans `EquipWeapon` apres refonte Radial Menu
- `ComboStepMap` vide car `InitComboTree` non appele a l'equipement
- `HandleAttack` tombait systematiquement dans ResetCombo (Map_Find retournait false)
- `LevelMin = 1` dans DT_Combo alors que `WeaponLevel = 0` -> filtre bloquant toutes les rows

#### Fixes BP_SoM_HeroCharacter -- EquipWeapon
- SET `ChoosenWeapon = RowName` apres SET CurrentWeapon
- `AddUnique(DiscoveredWeapons, RowName)` -- alimente la source de verite Radial
- Appel `BP_ComboManagerComponent.InitComboTree(WeaponID=RowName, WeaponLevel=0)`
- Ordre : SET CurrentWeapon -> SET ChoosenWeapon -> AddUnique -> InitComboTree -> AttachToComponent

#### Fixes BP_ComboManagerComponent -- HandleAttack
- Suppression du parametre `ChoosenWeapon` de la signature (inutile, le manager lit `CurrentWeaponID` en interne)

#### Fixes DT_Combo (Sword_01, 2HSword_01)
- `LevelMin` passe de 1 a 0 sur toutes les rows -- niveau de base = 0

#### Resultat VALIDE PIE
- Radial -> equipe arme -> InitComboTree charge ComboStepMap correctement
- Combo Light1 -> Light2 enchaine
- Heavy1 fonctionnel
- Degats appliques via AnimNotify EnableCollision/DisableCollision

#### Architecture validee (a conserver)
- `InitComboTree(WeaponID, WeaponLevel)` = unique point de chargement du ComboStepMap
- `CurrentWeaponID` + `CurrentWeaponLevel` sur ComboManager = source de verite combo
- `DiscoveredWeapons` sur HeroCharacter alimente par EquipWeapon = source de verite Radial
- `ChoosenWeapon` sur HeroCharacter = ID arme courante pour les inputs attaque

---

## Rappel
pour la roadmap detaillee : voir Docs/Roadmap_Gameplay.md
Pour le design UI/HUD/Menu : voir Docs/Architecture/UI_GlobalMenu.md

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 18/05/2026
