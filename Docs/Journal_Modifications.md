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
- Fix IsLockOnActive, fix dispatcher espace, fix bind PC, UpdateLockOnUIIndicator
- ABP_Manny_Platforming Strafe VALIDE PIE, edge cases valides

---

### 15/05/2026 -- J-Renommage COMPLET
- Convention nommage unifiee, Fix Up Redirectors, VALIDE PIE

---

### 17/05/2026 -- J-Camera COMPLET -- VALIDE PIE
- SpringArm regle, IA_Look dans PC, UpdateLockOnRotation V2, Screen Shake valide

---

### 18/05/2026 -- J-LockMove COMPLET -- VALIDE PIE
- Move() en lock-on via CameraRotation, Rotation Rate -1, LastAxisX/Y

---

### 18/05/2026 -- J-TestBed COMPLET -- VALIDE PIE
- Lvl_TestBed BSP, BP_Enemy_TestBed, SFX placeholder

---

### 18/05/2026 -- J-ComboFix COMPLET -- VALIDE PIE
- ChoosenWeapon, InitComboTree, HandleAttack sans parametre, LevelMin=0

---

### 18/05/2026 -- C1-CollisionFix COMPLET -- VALIDE PIE
- CapsuleComponent Pawn=Block, weapon collision audit

---

### 18/05/2026 -- C1-HitFeel PARTIEL -- VALIDE PIE
- Knockback + screen shake valides, hitstop reporte, vibration gamepad manque

---

### 19/05/2026 -- C1-HitFlashEnemies -- ARCHITECTURE COMPLETE
- Architecture DMI faite, blocage M_Mannequin identifie

---

### 21/05/2026 -- Session design & documentation
- C1-HitFlashEnemies ABANDONNE, C1-CleanupDettes 3/4, C1-InputsUI PRIORITAIRE
- Nouveau jalon C1-RadialMagie, Decisions.md cree, regles maintenance doc

---

### 23/05/2026 -- Session design -- Architecture IMC complete
- 5 IMC decides (Gameplay/Radial/Menu/Dialogue/Cutscene)
- IMC_Dialogue = SEUL cumulatif, personnage mobile pendant dialogues
- Cinematiques = Level Sequence -> IMC_Cutscene pertinent
- Corrections noms IA (audit T3D), IA_UI_Radial_Rotate identifiee

---

### 23/05/2026 -- C1-InputsUI COMPLET -- VALIDE PIE

#### IMC crees
- IMC_Gameplay (ex IMC_Prototype renomme) : charge au ReceivePossessed dans BP_SoM_HeroCharacter
- IMC_Radial : 4 IA navigation radial
- IMC_Menu, IMC_Dialogue, IMC_Cutscene : stubs vides

#### Swap IMC cable dans BP_SoM_PlayerController
- OpenRadial (apres SET bShowMouseCursor=true) :
  GetSubsystemFromPC(Self) -> RemoveMappingContext(IMC_Gameplay) -> AddMappingContext(IMC_Radial, Priority=1)
- CloseRadial (avant RemoveFromParent) :
  GetSubsystemFromPC(Self) -> RemoveMappingContext(IMC_Radial) -> AddMappingContext(IMC_Gameplay, Priority=0)

#### Fix rotation radial
- Bug : rotations multiples et sens incorrect au premier test
- Cause : axe analogique continu sans threshold -> declenchements en rafale
- Fix 1 : ajout trigger Pressed avec threshold 0.5 sur IA_UI_Radial_Rotate
- Fix 2 : ajout Modifier Negate X sur le binding direction gauche (Q / Stick G X-)
  Sans Negate, les deux directions envoient la meme valeur positive -> meme sens

#### Tests valides PIE
- Triangle -> inputs gameplay morts, radial naviguable
- Rotation gauche/droite correcte avec 3 armes
- Rond -> fermeture, inputs gameplay reviennent
- Attaque pendant radial ouvert -> rien
- IA_UI_Radial_Open toujours fonctionnel depuis le gameplay

---

## Rappel
Pour la roadmap detaillee : voir Docs/Roadmap_Gameplay.md
Pour les decisions architecturales : voir Docs/Architecture/Decisions.md
Pour les inputs et IMC : voir Docs/Architecture/Input_Architecture.md
Pour le radial menu : voir Docs/Architecture/RadialMenu_Architecture.md

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 23/05/2026
