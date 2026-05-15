# CLAUDE.md -- Shadow of Mana / Contexte IA

Ce fichier est lu par Claude au debut de chaque session pour retrouver le contexte du projet rapidement.
Il est lu aussi bien par Claude.ai (via GitHub MCP) que par l'agent UnrealClaude dans l'editeur UE5.7.

---

## Projet

- **Nom** : Shadow of Mana (SoM)
- **Genre** : ARPG Blueprint Only, inspire Secret of Mana + Dark Souls
- **Developpeur** : Nico (GitHub : Yazooalvein)
- **Repo** : https://github.com/Yazooalvein/SoM_250617
- **Moteur** : Unreal Engine 5.7.4

---

## Setup technique actuel Claude <> Projet

- **UnrealClaude v1.4.5** (plugin dans Plugins/UnrealClaude/)
  - Authentification via `claude auth login` (compte Anthropic Pro -- pas d'API key separee)
  - MCP bridge Node.js port 3000 (auto-start au lancement editeur)
  - 28 outils MCP natifs : Blueprint, AnimBlueprint, Enhanced Input, Material, Actor, Level, Asset...
  - Panel : Tools -> Claude Assistant dans l'editeur UE5.7
  - Facturation : incluse dans forfait Pro claude.ai (verifiable via `claude auth status`)
- **GitHub MCP** : node.exe --use-system-ca + NODE_TLS_REJECT_UNAUTHORIZED=0
- **Claude** : plan Pro, memoire activee

---

## Workflow dual-agent

### Roles
**Claude.ai** : chef de projet, planification, decisions archi, mise a jour docs via GitHub MCP
**Agent UnrealClaude** : discovery/audit Blueprint uniquement (pas de modif/creation), logue dans Session_UnrealClaude.md

### Regles
1. Nico pushe toujours en premier, Claude.ai committe la doc ensuite
2. L'agent UE logue ses actions dans Docs/Session_UnrealClaude.md en temps reel
3. Claude.ai lit Session_UnrealClaude.md en debut de session

---

## Instructions pour l'agent UnrealClaude

### Ligne de contexte OBLIGATOIRE dans chaque prompt
```
CONTEXTE : Tu es l'assistant UnrealClaude lance dans UE5.7 depuis "Tools => Claude Assistant", tu as acces a 28 MCP Tools.
```
Sans cette ligne, l'agent se croit dans Claude Code CLI et n'utilise pas ses outils MCP.

### Regles agent
- blueprint_query UNIQUEMENT. Jamais blueprint_modify, jamais execute_script.
- JAMAIS creer d'assets AnimGraph via MCP (add_state produit des shells corrompus)
- Toute creation d'etat AnimGraph = manuelle dans l'editeur
- Agent = discovery/audit uniquement. Pas de creation, pas de modification.
- Ouvrir une NOUVELLE session a chaque fois (pas continuer une ancienne)

### Logging obligatoire
Format dans Docs/Session_UnrealClaude.md :
```
### [DATE] -- [NOM DU BLUEPRINT / ASSET]
**Action** : ce qui a ete fait
**Pourquoi** : raison ou contexte
**Points d'attention** : gotchas, dependances
```

### Conventions architecture (IMPERATIVES)
- `SetStatValue(StatName, Value)` = UNIQUE point de modification des stats
- `OnStatChanged` = dispatcher de notification
- `BP_SoM_GameMode` : Player Controller Class = BP_SoM_PlayerController
- Hit Flash ennemi : DMI au BeginPlay, pas Set Scalar on Materials
- Inputs : source unique Content/Input/InputActions/

---

## Architecture cle

### Personnage
- `BP_SoM_HeroCharacter` (Blueprint Only, ex BP_PlatformingCharacter)
- Stats via `BP_AttributeSet_Base` (ref : `AttributeSetRef`)
- `bIsDead` (private) + `IsDead()` (public pure)
- `bIsInvincible` (iframes dash/roll, pilote par AnimNotify)
- `OnPlayerDeath` dispatcher, `OnStatChanged` dispatcher
- `DiscoveredWeapons` (Array<FName>) : source de verite dans PC
- `BP_CombatLockOnComponent` : sur le CHARACTER (pas le PC)
- `MagicComponent` : BP_MagicComponent sur le Character
- `BP_ComboManagerComponent` : sur le Character

### Hero 3D
- ABP actif : **ABP_Manny_Platforming** (pas ABP_Unarmed qui est pour les ennemis)
- Mesh : Meshy_AI_Crimson_Scarf_Adventu_0513214252_texture (Content/Characters/Players/Hero_Test/)
- Retargeting : Mannequin source -> Hero target (Compatible Skeletons)
- Variables ABP_Manny_Platforming : Character, MovementComponent, Velocity, GroundSpeed,
  ShouldMove, IsFalling, WeaponType, Strafe, Can Strafe, Double/Wall Jump...
- ⚠️ 246K triangles LOD0 -> retopo (cible 10-15K) -- J-ART final
- ⚠️ 6 doigts par main (artefact Meshy) -- J-ART final

### Lock-On -- J-lock COMPLET VALIDE PIE (15/05/2026)
- `BP_CombatLockOnComponent` : sur le Character, architecture propre
  - bisLockOnActive, CurrentTarget, AvailableTargets, LockOnRange, SwitchCooldown
  - OnLockOnActivated / OnLockOnDeactivated (dispatchers custom -- pas les events systeme)
  - DetectAvailableTargets (SphereOverlap + filtres IsDead/IsValid/Distance)
  - SelectInitialTarget (tri par distance), SwitchLockOnTarget (cooldown + angle DotProduct)
  - HandleTargetDeath (auto-switch ou delock), UpdateLockOnRotation (dans PC, RInterp vers cible)
  - ⚠️ TargetActor dans UI_LockOnIndicator a un espace dans son nom ("TargetActor ")
- `BP_SoM_PlayerController` (ex BP_PlatformingPlayerController) :
  - UpdateLockOnRotation : Find Look At Rotation + RInterp To + Set Control Rotation (Speed=30)
  - UpdateLockOnUIIndicator : gestion widget indicateur
  - LockOnPitchMin/Max : contraintes pitch camera configurable
  - ⚠️ Doublon cooldown switch : LockOnSwitchCooldown (PC) + SwitchCooldown (Component) -- a unifier
- `BP_SoM_HeroCharacter` bindings (au BeginPlay) :
  - OnLockOnActivated_Handler : bOrientRotationToMovement=false + UseControllerRotationYaw=true
  - OnLockOnDeactivated_Handler : bOrientRotationToMovement=true + UseControllerRotationYaw=false
- Strafe VALIDE PIE :
  - ABP_Manny_Platforming : Strafe (DotProduct Velocity/RightVector) + Can Strafe (NOT bOrientRTM)
  - State Machine : etat LockedOn_Strafe avec BS_Unarmed_Strafe
  - BS_Unarmed_Strafe : Content/Characters/Mannequins/Anims/Unarmed/ (Forward x Strafe [-1,1])
  - Animations placeholder : MF_Unarmed_Jog_Left pour gauche ET droite -- a affiner en J-B
- Dettes reportees J-Camera :
  - Switch cible : comportement a revoir en profondeur (KH style)
  - Fix z-order indicateur (AddToViewport ZOrder=10 dans UpdateLockOnUIIndicator)
  - Unification cooldown switch PC/Component

### Ennemis
- `BP_Enemy_Base` (ex BP_EnemyBase) : bCanBeLocked, bIsDead, OnDeath, bIsLocked, bIsAttacking, bHasAlreadyHit
  - MaxHealth/CurrentHealth (pas via SetStatValue -- coherent pour ennemis)
  - AttackRadius (ExposeOnSpawn), WeaponClass (hardcode BP_Enemy_Sword01 -- a generaliser J-EnemyArt)
  - EquipWeapon, EnableWeaponCollision, DisableWeaponCollision, KillMeNow (debug)
  - Implements BPI_TakeDamage
- `BP_AIController_Enemy_Base` : Behavior Tree + PawnSensing
- `BB_Enemy_Base` (ex BB_enemy) : Blackboard ennemi
- `BT_Enemy_Base` (ex BT_Enemy) : Behavior Tree ennemi
- `BP_Enemy_Test` (ex BP_enemyTest) : ennemi de test
- `BP_Enemy_Knight` : essai conserve de cote
- ABP_Unarmed : pour les ENNEMIS SANS ARME (pas le hero)
  - Strafe calcule via DotProduct -- ne pas modifier pour le hero

### Combat
- `BP_ComboManagerComponent` : architecture TMap<Name, FComboStep> -- a conserver
  - InitComboTree(WeaponID, WeaponLevel), HandleAttack, PlayAttackMontage, ResetCombo
  - RotateTowardLockTarget (deja present), GetBP_CombatLockOnComponent
  - UpgradeWeaponLevel -- aligne avec la future forge
- `BPI_TakeDamage` : interface implementee par Character et Enemy_Base
- ReceiveDamage : bIsInvincible? -> IsDead? -> SetStatValue("HealthCurrent") -> HitFlash -> mort?
- ⚠️ Logique combo/armes dans PC EventGraph supprimee (J-Nettoyage) -- refaire en J-15/16/17

### Armes
- `BP_Weapon_Base` : WeaponData (FWeaponData, ExposeOnSpawn), OwnerCharacter, bIsEquipped
  - bCanDealDamage, TouchedActors (anti-multi-hit), WeaponCollisionBox
  - OnEquipped/OnUnequipped (hooks overridables), EnableWeaponCollision, DisableWeaponCollision
  - TryDealDamage sur BeginOverlap
- `BP_Weapon_Sword` : herite BP_Weapon_Base, quasi-vide (CallParentFunction) -- bon pattern
- `DT_Weapons` : 2 entrees (Sword_01, 2HSword_01), struct FWeaponData
- `EquipWeapon(RowName)` dans BP_SoM_HeroCharacter
- ⚠️ Refonte armes prevue J-15/16/17 (BP_WeaponType_Base par TYPE)
- ⚠️ DiscoveredWeapons dans PC ET Character -- a unifier J-15/16/17

### GameMode / Controllers
- `BP_SoM_GameMode` (`/Game/Core/`) -- Player Controller Class = BP_SoM_PlayerController
- `BP_SoM_PlayerController` (ex BP_PlatformingPlayerController) :
  - Lock-On : GetBP_CombatLockOnComponent, UpdateLockOnRotation, UpdateLockOnUIIndicator
  - Radial Menu : Open/CloseRadial, Handle_Rotate, Handle_ChangeCat, ToggleRadial
  - Quickslots : QuickslotUp/Left/Right (FName)
  - PlayerCharacterRef, RadialMainRef, LockOnIndicatorWidgetRef
  - IsValid(RadialMainRef) guard OBLIGATOIRE avant tout appel radial

### Radial Menu -- J-13 COMPLET
- Assets actifs : ERadialMode, FSoM_RadialSlotData, UI_Radial_Main, UI_RadialSlot
- UI_Radial_Main : GenerateSlots, UpdateCenterInfo, UpdateSelection, PopulateWeaponSlots,
  SwitchCategory, ValidateSelectedWeapon -- VALIDE PIE

### Magie
- `BP_MagicComponent` : UnlockedSpells, QuickslotSlots, SpellCooldowns, CastSpell
- `BP_SpellBase` + 4 sorts Lumina valides PIE (Heal, Attack, Buff, Debuff)
- `DT_Spells` + structs FSoM_SpellData / FSoM_DeitySpells

### UI / HUD
- `UI_HUD_Main` : event-driven via OnStatChanged, zero polling -- FINALISE
- `UI_LockOnIndicator` : 1 image LockOnCross, tous events desactives -- widget statique positionne par PC
  - ⚠️ TargetActor a un espace dans son nom
  - ⚠️ Z-order : ajouter ZOrder=10 sur AddToViewport dans UpdateLockOnUIIndicator

### Data / Structs
- `DT_Combo_Base` (ex Datatable_FCombo) : DataTable combo de base
- `DT_Combo_Sword` / `DT_Combo_2HSword` : combos par arme
- `DT_StatList` (ex Datatable_StatList) : liste des stats
- `FComboStep`, `EAttackInputType` : structs/enums combo
- `EStatType`, `EElementType`, `StatStruct` : structs/enums stats

### Mapping Gamepad PS5 (ACTE)
```
X=Saut  Carre=Esquive  Rond=Blocage  Triangle=Radial
L1=Attaque legere  R1=Attaque forte
L2=Action PNJ compagnon 1  R2=Action PNJ compagnon 2
L3=Sprint  R3=Lock-On (axis=changer cible)
Fleche Haut/Gauche/Droite=Quickslots 1/2/3  Fleche Bas=Switch page
Options=Menu Global  Touchpad=TBD
```

### Inputs
- Source unique : Content/Input/InputActions/
- ⚠️ Dette : creer IMC_UI dedie pour inputs menus (J-C)

---

## Jalons completes

- [x] #1 a #9 : MCP, mort, stats, inputs, iframes, UI, hit flash, migration UE5.7, audit
- [x] J-10 a J-14 : BP_MagicComponent + 4 sorts Lumina valides PIE
- [x] J-15 : UI_HUD_Main finalise
- [x] J-13 : Radial Menu complet + Quickslot POC VALIDE PIE
- [x] J-Nettoyage : Suppression ancien radial, WeaponDataTest, assets obsoletes
- [x] J-ART (partiel) : Hero placeholder PIE, workflow etabli
- [x] J-MUS (exploration) : Workflow etabli, prompt theme sombre acte
- [x] J-lock COMPLET : Strafe VALIDE PIE, fix IsLockOnActive, fix dispatcher, edge cases valides
- [x] J-Renommage : Convention de nommage unifiee sur tous les assets cles

## Prochains jalons (ordre de dependances)

1. **J-Camera** : camera 3/4, collision, lock-on smooth (KH style), screen shake, hitstop
2. **J-TestBed** : mini zone BSP + BP_Enemy_TestBed + SFX placeholder
3. **J-SFX1** : sons de base (remonte en C1)
4. **J-15/16/17** : refonte armes + combo + unification DiscoveredWeapons
5. **J-C** : IMC_UI dedie
6. **J-F** : SaveGame
7. **J-18/19** : Arc + Weapon Switching
8. **J-B/E** : Animations + Hit Flash ennemis (+ rename ABP_Manny_Platforming -> ABP_Hero)

Sessions creatives intercalees : J-MAP / J-ART / J-MUS

---

## Workflows creatifs etablis

### J-ART -- Workflow hero 3D
```
Dessin crayon -> Leonardo.ai (Lucid Origin, guidance 8)
-> Gemini (vues complementaires) -> Meshy 5 (single image T-Pose)
-> AccuRIG -> Export FBX -> Import UE5
-> Compatible Skeletons + RTG Mannequin source -> Hero target
```
Points critiques : T-Pose mains ouvertes, bras ecartes, pas d'arme sur le mesh

### J-MUS -- Workflow theme musical
```
Fredonnement personnel -> Suno.ai (50 credits/jour)
-> Remix (slider style/fidelity) -> Export MP3 -> UE5 Sound Cue / MetaSound
```
Prompt : dark orchestral, 60 BPM, D minor, cello lead, no brass, sparse, desolate overworld

---

## Notes techniques importantes

- SetStatValue = unique point de modification stats
- ABP_Manny_Platforming = ABP du HERO (pas ABP_Unarmed qui est pour les ennemis)
- UpdateLockOnRotation dans PC = suivi camera vers cible (ne pas doublon dans Component Tick)
- Bind "On Lock on Activated/Deactivated" = dispatchers CUSTOM du Component
  (pas "On Component Activated/Deactivated" qui sont les events systeme UE)
- T3D export (clic droit -> Asset Actions -> Export) = meilleur outil d'audit
- add_state MCP dans AnimGraph = shell corrompu garanti -> toujours creer les etats manuellement
- PrintString : toujours rebrancher les pins exec avant de supprimer
- RichTextBlock : necessite DataTable RichTextStyleRow assignee
- Time Dilation 0.2 ouverture radial, 1.0 fermeture
- Radial drift fix : RadialContainer Size = 0.01x0.01
- RTG retargeting : toujours Mannequin SOURCE, hero TARGET

---

## Comment demarrer une session

### Session claude.ai
1. Nico dit : "on travaille sur SoM, lis le CLAUDE.md et le journal"
2. Claude.ai lit CLAUDE.md + Journal_Modifications.md + Session_UnrealClaude.md
3. Claude.ai fait un resume et propose la suite

### Session UnrealClaude (editeur)
1. Ouvrir Tools -> Claude Assistant -> NOUVELLE session
2. Commencer par : "CONTEXTE : Tu es l'assistant UnrealClaude lance dans UE5.7 depuis 'Tools => Claude Assistant', tu as acces a 28 MCP Tools."
3. Ajouter : "Lis le CLAUDE.md et logue tes actions dans Docs/Session_UnrealClaude.md"
4. Agent en mode DISCOVERY UNIQUEMENT -- pas de blueprint_modify

---

*Derniere mise a jour : 15/05/2026*
