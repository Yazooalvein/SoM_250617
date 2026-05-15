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
- BPI_TakeDamage, BP_EnemyBase ReceiveDamage + OnDeath

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
- UpdateCenterInfo : textes centre depuis SlotDataList[SelectedIndex]
- Fix surbrillance 12h a l'ouverture + drift (RadialContainer 0.01x0.01)
- Fix sens rotation : inversion signe accumulation TargetRotation
- Centrage : RadialRadius = 330, SizeBox padding left = -50
- Image_Cursor masquee (a faire plus tard)

#### PopulateWeaponSlots -- pont temporaire armes VALIDE PIE
- DiscoveredWeapons (Array<FName>) -> GetDataTableRow(DT_Weapons) -> FSoM_RadialSlotData
- Remplace les 4 slots hardcodes dans Event Construct

#### SwitchCategory -- VALIDE PIE
- Toggle CurrentCategory Weapons <-> Magic
- Reset SelectedIndex/TargetRotation/CurrentRotation = 0 au switch
- IA_UI_RadialMenu_ChangeCat -> Handle dans PC avec IsValid guard

#### ValidateSelectedWeapon -- VALIDE PIE
- Migre depuis UI_RadialMenu vers UI_Radial_Main
- SlotDataList[SelectedIndex].SlotID -> EquipWeapon -> CloseRadialMenu
- IA_validate_radial_selection avec IsValid guard dans PC

#### Cancel -- VALIDE PIE
- IA_UI_Radial_Cancel -> IsValid(RadialMainRef) -> CloseRadialMenu
- Note : a terme migrer vers IMC_UI dedie (dette)

#### Quickslot POC -- VALIDE PIE
- 3 variables dans PC : QuickslotUp/Left/Right (FName, SpellID)
- IA_Quickslot_Up/Left/Right -> CastSpell via MagicComponent
- Mapping clavier : & (1) / e accent (2) / guillemet (3)
- Mapping gamepad prevu : fleches haut gauche droite (bas = switch page futur)

#### Session design actee (13/05/2026)
- Mapping PS5 complet acte (voir Docs/Architecture/UI_GlobalMenu.md)
- Quickslot : 3 slots, multi-pages via fleche bas, choix strategique (4 sorts / 3 slots)
- Roadmap reorganisee par dependances + sessions creatives (J-MAP / J-ART / J-MUS)
- Lock-On : dette confirmee (J-lock entre J-13 et J-15)
- Arc : munitions illimitees ACTE

---

### 14/05/2026 -- Session creative J-MUS (exploration workflow)

#### Workflow MP3 -> MIDI -> transformation explore
- Basic Pitch (Spotify) : conversion MP3 -> MIDI validee, gratuit, navigateur
- AIVA.ai : teste pour transformation MIDI -> orchestration sombre -- resultats insuffisants
- Workflow retenu pour J-MUS futur :
  - Humming / fredonnement -> Suno (gratuit, 50 credits/jour)
  - Suno Covers : transformation style avec preservation melodique
  - Suno Remix : iterations plus sombre / autre instru par slider
  - Export MP3 -> import UE5 (Sound Cue / MetaSound)
- Prompt Suno etabli pour le theme overworld sombre (monde devaste, cordes graves, 60 BPM)
- Theme Seiken Densetsu 1 : source protegee, workflow via fredonnement personnel uniquement

---

### 14/05/2026 -- Session creative J-ART -- Hero PLACEHOLDER COMPLET

#### Workflow etabli et teste
- Dessin crayon (Nico) -> Leonardo.ai -> Gemini -> Meshy 5 -> AccuRIG -> UE5.7
- IK Rig + RTG (Mannequin source -> Hero target) -- VALIDE PIE
- M_Hero_Body (material PBR + HitFlash)

#### Design hero valide -- palette finale ACTEE
- Cheveux brun fonce, echarpe rouge cramoisi, armure gris anthracite
- Veste bleu nuit, pantalon marron sombre, bottes+gants noirs
- Lanieres croisees en X marron cuir, Medaillon Mana centre poitrine

#### Dettes J-ART restantes
- 6 doigts -> 5 dans Blender, retopo (246K -> cible 10-15K), LODs
- Sockets HandGrip_R/L a affiner, armes comme assets separes

---

### 14/05/2026 -- J-Nettoyage COMPLET

#### Suppressions effectuees
- BP_PlatformingCharacter : WeaponDataTest supprimee
- BP_PlatformingPlayerController : RadialMenuRef, SlotRowNames, SlotIcons supprimes
- Assets : UI_RadialMenu, UI_RadialSlot_old, BP_PlatformingGameMode, BP_test_IA
- Reorganisation dossier Enemies (Animations/, Model/, Blueprints/)

---

### 14/05/2026 -- Session design -- Roadmap globale refondee
- ~50 jalons, 8 couches, projet complet de A a Z
- Decisions : FR+EN des le debut, tuto minimaliste, vibration standard
- Ordre revise : J-lock -> J-Camera -> J-TestBed -> J-15/16/17

---

### 15/05/2026 -- J-lock PARTIEL -- Strafe fonctionnel

#### Corrections BP_CombatLockOnComponent
- Fix `IsLockOnActive` : retourne desormais `bisLockOnActive` (etait vide)
- Fix espace dans dispatcher : `OnLockOnDeactivated ` -> `OnLockOnDeactivated` (espace supprime)
- Lecon : exporter en T3D pour audit complet -- revele les bugs invisibles en screenshot

#### Corrections BP_PlatformingPlayerController
- Fix `Bind Event to On Lock on Deactivated` : rebind apres correction du nom du dispatcher
- Attention : utiliser "Bind Event to On Lock on Activated/Deactivated" (dispatchers custom)
  et NON "Bind Event to On Component Activated/Deactivated" (events systeme generiques)

#### Corrections BP_PlatformingCharacter
- Ajout bindings OnLockOnActivated/Deactivated au BeginPlay :
  - OnLockOnActivated_Handler : bOrientRotationToMovement=false + UseControllerRotationYaw=true
  - OnLockOnDeactivated_Handler : bOrientRotationToMovement=true + UseControllerRotationYaw=false
- Source du composant : BP_CombatLockOnComponent est sur le CHARACTER (pas le PC)

#### Corrections ABP_Manny_Platforming (ABP du hero)
- Ajout variables : `Strafe` (float) + `Can Strafe` (bool)
- Event Update Animation -> nouveau Then : calcul DotProduct + NOT bOrientRotationToMovement
  - Utilise directement `Character` et `MovementComponent` (references deja stockees dans l'ABP)
- State Machine Locomotion : ajout etat `LockedOn_Strafe`
  - Transitions : Idle/Walk <-> LockedOn_Strafe sur Can Strafe
  - BS_Unarmed_Strafe assigne (Ground Speed -> Forward, Strafe -> Strafe)
  - Animations placeholder : MF_Unarmed_Jog_Left pour les deux cotes (a affiner en J-B)

#### BS_Unarmed_Strafe (cree manuellement)
- Chemin : Content/Characters/Mannequins/Anims/Unarmed/
- Axes : Forward [-1,1] x Strafe [-1,1]
- Points : MM_Idle(0,0), Jog_Fwd(1,0), Jog_Bwd(-1,0), Jog_Left(-1,0 et +1,0 placeholder)
- ⚠️ Animations strafe gauche/droite distinctes : a faire en J-B

#### ABP_Unarmed -- nettoyage
- Strafe/Can Strafe/LockedOn_Strafe ajoutes par erreur puis retires
- ABP_Unarmed = ennemis sans arme (pas le hero) -- ne pas modifier pour le hero

#### Caution UpdateLockOnRotation
- SetControlRotation vers la cible est DEJA gere dans PC -> UpdateLockOnRotation
- Ne pas doublon dans BP_CombatLockOnComponent Tick (conflit detecte et corrige)

#### Dettes J-lock restantes
- Fix z-order indicateur lock-on (UI_LockOnIndicator passe derriere le HUD)
  - Fix : AddToViewport avec ZOrder=10 dans UpdateLockOnUIIndicator du PC
  - Aussi : TargetActor a un espace dans son nom ("TargetActor ") -> a corriger
- Unification cooldown switch : doublon entre PC (LockOnSwitchCooldown) et Component (SwitchCooldown)
- Tests edge cases : mort ennemi, switch cible, delock

#### Audit T3D complet effectue
Fichiers analyses : BP_CombatLockOnComponent, BP_PlatformingPlayerController,
BP_PlatformingCharacter, ABP_Manny_Platforming, ABP_Unarmed, BP_EnemyBase,
UI_LockOnIndicator, BP_Weapon_Base, BP_Weapon_Sword, BP_ComboManagerComponent

Points cles decouverts :
- BP_ComboManagerComponent : architecture TMap solide, a conserver pour J-15/16/17
  - RotateTowardLockTarget existe deja dans le ComboManager
  - InitComboTree(WeaponID, WeaponLevel) : parfaitement aligne avec la future forge
- BP_Weapon_Base : OnEquipped/OnUnequipped hooks overridables, TouchedActors anti-multi-hit
- BP_Weapon_Sword : quasi-vide (CallParentFunction uniquement) -- bon pattern a continuer
- BP_EnemyBase : WeaponClass hardcode sur BP_Enemy_Sword01 -> a rendre generique en J-EnemyArt
- UI_LockOnIndicator : widget minimal (1 image LockOnCross), tous events desactives

---

## Rappel
Pour la roadmap detaillee : voir Docs/Roadmap_Gameplay.md
Pour le design UI/HUD/Menu : voir Docs/Architecture/UI_GlobalMenu.md

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 15/05/2026
