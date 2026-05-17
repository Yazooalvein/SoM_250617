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

### 14/05/2026 -- Session creative J-ART -- Hero PLACEHOLDER COMPLET
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
- Mort ennemi : delock/switch automatique ✅
- Switch cible (stick droit) : fonctionnel ✅ (a revoir en J-Camera)
- Delock manuel (R3) : retour locomotion normale ✅
- Delock hors range ✅
- Indicateur positionne au-dessus de la tete ✅
- Indicateur masque si hors frustum ✅

#### Dettes reportees J-Camera
- Switch cible : comportement a revoir en profondeur (KH style)
- Fix z-order indicateur (AddToViewport ZOrder=10 dans UpdateLockOnUIIndicator)
- Unification cooldown switch PC/Component
- Animations strafe gauche/droite distinctes : J-B
- TargetActor espace dans UI_LockOnIndicator : cosmetique, a corriger

#### Design note J-Camera (lock-on)
- Camera KH style : suit activement pour garder la cible lockee visible
- Delock automatique si cible hors champ (couloir, hauteur) -- DS style
- Marqueur a repenser : cercle au sol / fleche / autre image (pas juste LockOnCross)

#### Audit T3D complet effectue
- BP_ComboManagerComponent : architecture TMap solide, a conserver (InitComboTree aligne avec forge)
- BP_Weapon_Base/Sword : pattern propre, OnEquipped/OnUnequipped overridables
- BP_Enemy_Base : WeaponClass hardcode -> a generaliser en J-EnemyArt
- UI_LockOnIndicator : widget statique minimal (1 image), positionne par PC via Set Position in Viewport

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
  - SET bPlayerIsLooking = true + SET LookIdleTime = 0.0
  - Get Controlled Pawn -> AddControllerYawInput (Axis X)
  - Get Controlled Pawn -> AddControllerPitchInput (Axis Y)
- IA_Look retire de BP_SoM_HeroCharacter
- IA_Look Triggered -> Aim | IA_Look Completed -> SET bPlayerIsLooking = false
- VALIDE PIE

#### Nouvelles variables BP_SoM_PlayerController
- `bPlayerIsLooking` (bool, false) : stick droit actif ce frame
- `LookIdleTime` (float, 0.0) : temps ecoule depuis dernier input Look
- `LookReturnDelay` (float, 1.5, expose) : delai avant retour camera vers ennemi
- `LockOnReturnSpeed` (float, 3.0, expose) : vitesse RInterp retour vers ennemi

#### UpdateLockOnRotation V2 -- VALIDE PIE
- Logique conditionnelle remplace SetControlRotation systematique :
  - Branch (bPlayerIsLooking) -> True : exit (joueur controle la camera)
  - Branch (LookIdleTime >= LookReturnDelay) -> True : SetControlRotation, False : exit
- RInterpTo InterpSpeed branche sur LockOnReturnSpeed (3.0) au lieu de hardcode 30
- Data flow RInterpTo -> SetControlRotation intact

#### Event Tick -- LookIdleTime
- Apres UpdateLockOnUIIndicator : Branch (bisLockOnActive AND IsValid(Widget) AND NOT bPlayerIsLooking)
  -> True : LookIdleTime += DeltaSeconds

#### Checklist validation J-Camera
- Hors lock-on : camera repond normalement ✅
- Lock-on, stick droit au repos : camera revient vers ennemi apres ~1.5s ✅
- Lock-on, joueur pivote stick droit : camera suit librement ✅
- Screen shake visible (coups recus + mort ennemi) ✅
- Dash/Roll : guard NOT Is Dashing/Rolling en place ✅

#### Dette J-LockMove -- reportee
- En lock-on, dash et roll partent vers l'ennemi
- Cause : Move() utilise Get Control Rotation -> GetForwardVector/GetRightVector
- Pistes : IMC dedie lock-on, ou dissocier direction deplacement de Control Rotation

---

## Rappel
Pour la roadmap detaillee : voir Docs/Roadmap_Gameplay.md
Pour le design UI/HUD/Menu : voir Docs/Architecture/UI_GlobalMenu.md

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 17/05/2026
