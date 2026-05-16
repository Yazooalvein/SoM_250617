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

### 16/05/2026 -- J-Camera EN COURS

#### Fixes permanents (gardes apres rollback)
- `BP_SoM_PlayerController` On Possess : SET PlayerCharacterRef depuis Possessed Pawn (Cast to BP_SoM_HeroCharacter)
  - Bug : PlayerCharacterRef etait None -> erreurs runtime au Tick
- Tick PC : guard `NOT Is Dashing / NOT Is Rolling` ajoute dans le AND de condition UpdateLockOnRotation
  - Empeche UpdateLockOnRotation d'ecraser la rotation pendant dash/roll

#### SpringArm ajuste (BP_SoM_HeroCharacter)
- Target Arm Length : 400 -> 350
- Socket Offset Z : 0 -> 60
- Camera Lag Speed : 16 -> 8
- Camera Lag Max Distance : 0 -> 200
- (valeurs a affiner au feeling en jeu)

#### Dette J-LockMove -- reportee apres J-Camera
- Probleme : en lock-on, dash et roll partent toujours vers l'ennemi
- Cause identifiee : `AddMovementInput` dans Move() utilise GetForwardVector/GetRightVector
  depuis Get Control Rotation -- qui pointe vers l'ennemi en lock-on.
  Le Root Motion du montage pousse donc toujours dans cette direction.
- Pistes a explorer en J-LockMove :
  - Stocker la direction du stick en espace monde AVANT que le lock-on influence la Control Rotation
  - Revoir la fonction Move() pour dissocier la direction de deplacement de la Control Rotation en lock-on
  - Potentiellement : IMC dedie lock-on avec IA_Move_LockOn calculant Forward/Right depuis
    une rotation camera "propre" (Yaw only, independante du lock)
- Rollback effectue : aucune modification du flow dash/roll n'est conservee (sauf les deux fixes ci-dessus)

---

## Rappel
Pour la roadmap detaillee : voir Docs/Roadmap_Gameplay.md
Pour le design UI/HUD/Menu : voir Docs/Architecture/UI_GlobalMenu.md

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 16/05/2026
