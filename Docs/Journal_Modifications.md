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
- Fix IsLockOnActive : retourne desormais bisLockOnActive (etait vide)
- Fix espace dans dispatcher : OnLockOnDeactivated(espace) -> OnLockOnDeactivated

#### Fixes BP_SoM_PlayerController
- Fix bind dispatcher custom OnLockOnActivated/Deactivated
- UpdateLockOnUIIndicator : SetVisibility selon Project World to Screen bool
- Socket indicateur lock-on deplace au-dessus de la tete

#### Fixes BP_SoM_HeroCharacter
- Bindings OnLockOnActivated/Deactivated au BeginPlay
- ABP_Manny_Platforming -- Strafe VALIDE PIE

#### Tests edge cases VALIDES PIE
- Mort ennemi, switch cible, delock manuel, delock hors range

---

### 15/05/2026 -- J-Renommage COMPLET
- Convention nommage unifiee : BP_SoM_HeroCharacter, BP_SoM_PlayerController, etc.
- Renames via UE Rename + Fix Up Redirectors, VALIDE PIE

---

### 17/05/2026 -- J-Camera COMPLET -- VALIDE PIE
- SpringArm : Arm 350, OffsetZ 60, Lag 8, MaxDist 200
- IA_Look deplace dans BP_SoM_PlayerController (fonction Aim)
- UpdateLockOnRotation V2 : conditionnel, bPlayerIsLooking, LookReturnDelay
- Screen Shake : CS_HitReceived + CS_EnemyDeath VALIDES PIE
- Fix PlayerCharacterRef SET au OnPossess

---

### 18/05/2026 -- J-LockMove COMPLET -- VALIDE PIE
- Move() en lock-on : GetPlayerCameraManager -> GetCameraRotation -> Yaw
- LastAxisX / LastAxisY stockes au Triggered de IA_Move
- Rotation Rate Z = -1 (pivot instantane hors lock-on)
- Dette roll en lock-on -> reporte C1-AnimationsPass1

---

### 18/05/2026 -- J-TestBed COMPLET -- VALIDE PIE
- Lvl_TestBed : BSP 4000x4000, NavMesh, lighting Movable, GameMode Override
- BP_Enemy_TestBed : stats Instance Editable, herite BP_Enemy_Base
- SFX placeholder : hit joueur, attaque ennemi, roll hero

---

### 18/05/2026 -- J-ComboFix COMPLET -- VALIDE PIE
- SET ChoosenWeapon dans EquipWeapon
- InitComboTree appele a l'equipement
- HandleAttack : suppression parametre ChoosenWeapon
- LevelMin = 0 sur toutes les rows DT_Combo

---

### 18/05/2026 -- Resynchro documentation complete
- Roadmap_Gameplay.md et CLAUDE.md : jalons completes coches, convention C1/C2/...
- Nouveaux jalons : C1-CollisionFix, C1-HitFlashEnemies, C1-HitFeel,
  C1-CleanupDettes, C1-WeaponArchitecture, C1-SaveDesign, C2-SaveGame

---

### 18/05/2026 -- C1-CollisionFix COMPLET -- VALIDE PIE

#### Capsules qui se traversent
- Fix : BP_SoM_HeroCharacter + BP_Enemy_Base -> CapsuleComponent -> Pawn = Block
- Resultat : pawns se poussent correctement, feeling combat ameliore

#### Weapon Collision
- Audit BP_Weapon_Base : presets coherents, guard OwnerCharacter verifie
- Clear Array dans DisableWeaponCollision confirme

---

### 18/05/2026 -- C1-HitFeel COMPLET (partiel) -- VALIDE PIE

#### Screen Shake -- 3 bugs corriges
1. ClientStartCameraShake inutilisable depuis Character en Single Player PIE
   -> Fix : GetPlayerController(0) -> GetPlayerCameraManager -> StartCameraShake
2. PlaySpace = World rendait le shake invisible
   -> Fix : PlaySpace -> CameraLocal
3. Rotation Amplitude Multiplier = 0.0 annulait toutes les rotations
   -> Fix : Rotation Amplitude Multiplier -> 1.0

#### Valeurs CS_HitReceived (a affiner)
- Rotation Amplitude Multiplier 1.0, Pitch 3.0 / Yaw 1.0 / Roll 2.0 / Freq 20.0
- Duration 0.3, Blend In 0.05, Blend Out 0.1

#### Valeurs CS_EnemyDeath (a affiner)
- Rotation Amplitude Multiplier 1.0, Pitch 5.0 / Yaw 2.0 / Roll 3.0 / Freq 15.0
- Duration 0.5, Blend In 0.05, Blend Out 0.2

#### Knockback ennemi -- VALIDE PIE
- BP_Enemy_Base -> ReceiveDamage : GetActorLocation(Ennemi) - GetActorLocation(Hero)
- Normalize -> * 400.0 -> LaunchCharacter(bXYOverride=true, bZOverride=false)
- 400.0 a tuner selon feeling

#### Hitstop -- REPORTE
- Necessite animations hit reaction + vrais SFX pour evaluer l'interet
- Reference : Dark Souls feedback via son + animation stagger, pas de hitstop global
- A reevaluer apres C2-EnemyMesh + C1-SFXCombat

---

### 19/05/2026 -- C1-HitFlashEnemies -- ARCHITECTURE COMPLETE (flash visuel en attente)

#### Architecture DMI BP_Enemy_Base
- Variable `HitFlashDMIs` : Array<Material Instance Dynamic>, private
- BeginPlay : ForLoop sur GetNumMaterials -> GetMaterial(Index) -> CreateDMI -> ADD to HitFlashDMIs
  -> Architecture generique, fonctionne avec n'importe quel mesh/material sans modification
- Fonction `TriggerHitFlash(ScalarValue : float)` : ForEach HitFlashDMIs -> SetScalarParameterValue("HitFlashAmount", Value)
- ReceiveDamage : TriggerHitFlash(1.0) -> Delay 0.12s -> TriggerHitFlash(0.0)
- Anciens noeuds SetScalarParameterValueOnMaterials (ErrorType=1) supprimes et remplaces

#### Material M_Mannequin
- ScalarParameter `HitFlashAmount` confirme present dans M_Mannequin (Emissive : HitFlashAmount * (50,50,50))
- Flash visuel non visible en PIE : M_Mannequin est un material Engine partage (read-only en runtime)
- DETTE : dupliquer M_Mannequin -> Content/Characters/Enemies/Materials/M_Enemy_Base
  et l'assigner au mesh ennemi pour debloquer le flash visuel

#### Notes architecture
- TriggerHitFlash est une fonction BP (pas de Delay dedans -- Delay reste dans EventGraph)
- GetMaterial au lieu de hardcoder Source Material -> prod-ready, zero modif par ennemi
- SKM_Manny_Simple utilise pour POC (2 slots : M_HeadLegs + M_Torso, les deux M_Mannequin)

---

## Rappel
Pour la roadmap detaillee : voir Docs/Roadmap_Gameplay.md
Pour le design UI/HUD/Menu : voir Docs/Architecture/UI_GlobalMenu.md

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 19/05/2026
