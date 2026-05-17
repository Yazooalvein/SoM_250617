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
- Rotation Rate Z = -1 (pivot instantane hors lock-on)
- Variables LastAxisX, LastAxisY (double) : stockees au Triggered de IA_Move
- ⚠️ 246K triangles LOD0 -> retopo (cible 10-15K) -- J-ART final
- ⚠️ 6 doigts par main (artefact Meshy) -- J-ART final

### Camera -- J-Camera COMPLET VALIDE PIE (17/05/2026)

#### SpringArm (BP_SoM_HeroCharacter)
- Target Arm Length : 350, Socket Offset Z : 60
- Camera Lag Speed : 8, Camera Lag Max Distance : 200

#### Screen Shake
- CS_HitReceived + CS_EnemyDeath dans Content/Systems/Camera/
- Appeles depuis ReceiveDamage (HeroCharacter) et KillMeNow (Enemy_Base)

#### IA_Look dans BP_SoM_PlayerController
- Fonction `Aim(Axis X, Axis Y)` dans le PC
- IA_Look RETIRE de BP_SoM_HeroCharacter

#### UpdateLockOnRotation V2
- Variables PC : bPlayerIsLooking (bool), LookIdleTime (float), LookReturnDelay (float, 1.5), LockOnReturnSpeed (float, 3.0)
- Guard supplementaire : Branch(Is Rolling) avant SetControlRotation -> si rolling, exit sans modifier
- Flow : DynamicCast -> Branch(IsRolling) -> Branch(bPlayerIsLooking) -> Branch(LookIdleTime >= LookReturnDelay) -> SetControlRotation

### J-LockMove COMPLET VALIDE PIE (18/05/2026)

#### Fix Move() en lock-on
- Probleme : en lock-on, deplacement partait vers l'ennemi (Control Rotation = direction ennemi)
- Solution : Branch(bisLockOnActive) dans Move() :
  - Lock-on actif : GetPlayerCameraManager -> GetCameraRotation -> Yaw -> MakeRotator(0,Yaw,0) -> GetForward/RightVector
  - Hors lock-on : comportement original (GetControlRotation)
- ScaleValues : branches sur LastAxisX/LastAxisY (stockees au Triggered de IA_Move)
- Deplacement en lock-on VALIDE PIE ✅

#### Fix rotation de base
- CharacterMovement -> Rotation Rate Z = -1 -> pivot instantane hors lock-on ✅

#### Roll en lock-on -- DETTE J-LockMove2
- Probleme : roll en lock-on part toujours vers l'ennemi
- Cause racine : Root Motion en World Space + UseControllerRotationYaw=true force
  le character a regarder l'ennemi chaque frame, annulant SetActorRotation
- Solution propre : LaunchCharacter dans direction stick+camera + animation visuelle sans Root Motion
  (architecture DS/KH) -- A traiter en J-B lors du chantier animations
- En attendant : roll hors lock-on fonctionne correctement ✅

### Lock-On -- J-lock COMPLET VALIDE PIE (15/05/2026)
- `BP_CombatLockOnComponent` : sur le Character
  - bisLockOnActive, CurrentTarget, AvailableTargets, LockOnRange, SwitchCooldown
  - OnLockOnActivated / OnLockOnDeactivated (dispatchers custom)
- `BP_SoM_HeroCharacter` bindings (au BeginPlay) :
  - OnLockOnActivated_Handler : bOrientRotationToMovement=false + UseControllerRotationYaw=true
  - OnLockOnDeactivated_Handler : bOrientRotationToMovement=true + UseControllerRotationYaw=false
- Strafe VALIDE PIE : BS_Unarmed_Strafe (Forward x Strafe [-1,1]), animations placeholder

### Ennemis
- `BP_Enemy_Base` : bCanBeLocked, bIsDead, OnDeath, bIsLocked, bIsAttacking, bHasAlreadyHit
  - WeaponClass (hardcode BP_Enemy_Sword01 -- a generaliser J-EnemyArt)
  - Implements BPI_TakeDamage
- `BP_AIController_Enemy_Base` : Behavior Tree + PawnSensing
- ABP_Unarmed : pour les ENNEMIS SANS ARME (pas le hero)

### Combat
- `BP_ComboManagerComponent` : architecture TMap<Name, FComboStep> -- a conserver
- `BPI_TakeDamage` : interface implementee par Character et Enemy_Base
- ReceiveDamage : bIsInvincible? -> IsDead? -> SetStatValue("HealthCurrent") -> HitFlash -> mort?

### Armes
- `BP_Weapon_Base` : WeaponData, OwnerCharacter, bIsEquipped, bCanDealDamage, TouchedActors
- `DT_Weapons` : 2 entrees (Sword_01, 2HSword_01), struct FWeaponData
- ⚠️ Refonte armes prevue J-15/16/17

### GameMode / Controllers
- `BP_SoM_GameMode` (`/Game/Core/`) -- Player Controller Class = BP_SoM_PlayerController
- `BP_SoM_PlayerController` :
  - PlayerCharacterRef : SET au OnPossess
  - Lock-On : GetBP_CombatLockOnComponent, UpdateLockOnRotation V2, UpdateLockOnUIIndicator
  - Aim(Axis X, Axis Y) : gestion camera

### Radial Menu -- J-13 COMPLET
- UI_Radial_Main : GenerateSlots, UpdateCenterInfo, UpdateSelection, PopulateWeaponSlots,
  SwitchCategory, ValidateSelectedWeapon -- VALIDE PIE

### Magie
- `BP_MagicComponent` : UnlockedSpells, QuickslotSlots, SpellCooldowns, CastSpell
- `BP_SpellBase` + 4 sorts Lumina valides PIE (Heal, Attack, Buff, Debuff)

### UI / HUD
- `UI_HUD_Main` : event-driven via OnStatChanged, zero polling -- FINALISE
- `UI_LockOnIndicator` : 1 image LockOnCross, widget statique positionne par PC

### Mapping Gamepad PS5 (ACTE)
```
X=Saut  Carre=Esquive  Rond=Blocage  Triangle=Radial
L1=Attaque legere  R1=Attaque forte
L3=Sprint  R3=Lock-On (axis=changer cible)
Fleche Haut/Gauche/Droite=Quickslots 1/2/3  Fleche Bas=Switch page
Options=Menu Global
```

---

## Jalons completes

- [x] #1 a #9 : MCP, mort, stats, inputs, iframes, UI, hit flash, migration UE5.7, audit
- [x] J-10 a J-14 : BP_MagicComponent + 4 sorts Lumina valides PIE
- [x] J-15 : UI_HUD_Main finalise
- [x] J-13 : Radial Menu complet + Quickslot POC VALIDE PIE
- [x] J-Nettoyage : Suppression assets obsoletes
- [x] J-ART (partiel) : Hero placeholder PIE, workflow etabli
- [x] J-MUS (exploration) : Workflow etabli
- [x] J-lock COMPLET : Strafe VALIDE PIE, fix IsLockOnActive, edge cases valides
- [x] J-Renommage : Convention de nommage unifiee
- [x] J-Camera COMPLET : UpdateLockOnRotation V2, bPlayerIsLooking, screen shake, IA_Look dans PC
- [x] J-LockMove COMPLET : Move() en lock-on corrige, Rotation Rate -1, LastAxisX/Y

## Dettes techniques

- **J-LockMove2** : roll en lock-on part vers l'ennemi (Root Motion World Space + UseControllerRotationYaw)
  -> Solution : LaunchCharacter + anim visuelle, a traiter en J-B
- ⚠️ Doublon cooldown switch : LockOnSwitchCooldown (PC) + SwitchCooldown (Component) -- a unifier
- ⚠️ TargetActor espace dans UI_LockOnIndicator ("TargetActor ")
- ⚠️ Z-order indicateur lock-on : ajouter ZOrder=10 sur AddToViewport
- ⚠️ IMC_UI dedie pour inputs menus : J-C
- ⚠️ Animations strafe gauche/droite distinctes : J-B
- ⚠️ WeaponClass hardcode BP_Enemy_Sword01 : J-EnemyArt
- ⚠️ Retopo hero 246K -> 10-15K : J-ART final
- ⚠️ rename ABP_Manny_Platforming -> ABP_Hero : J-B

## Prochains jalons (ordre)

1. **J-TestBed** : mini zone BSP + BP_Enemy_TestBed + SFX placeholder -- PRIORITE IMMEDIATE
2. **J-SFX1** : sons de base
3. **J-15/16/17** : refonte armes + combo + unification DiscoveredWeapons
4. **J-C** : IMC_UI dedie
5. **J-F** : SaveGame
6. **J-B/E** : Animations + Hit Flash ennemis (+ J-LockMove2)

---

## Notes techniques importantes

- SetStatValue = unique point de modification stats
- ABP_Manny_Platforming = ABP du HERO (pas ABP_Unarmed)
- UpdateLockOnRotation dans PC = suivi camera vers cible V2 (conditionnel)
- Bind "On Lock on Activated/Deactivated" = dispatchers CUSTOM du Component
- T3D export (clic droit -> Asset Actions -> Export) = meilleur outil d'audit
- add_state MCP dans AnimGraph = shell corrompu garanti -> toujours creer manuellement
- IA_Look est dans le PC (pas dans HeroCharacter) depuis J-Camera
- Move() en lock-on : utilise GetPlayerCameraManager -> GetCameraRotation (pas GetControlRotation)
- LastAxisX/LastAxisY : variables double sur HeroCharacter, SET au Triggered de IA_Move

---

## Comment demarrer une session

### Session claude.ai
1. Nico dit : "on travaille sur SoM, lis le CLAUDE.md et le journal"
2. Claude.ai lit CLAUDE.md + Journal_Modifications.md via GitHub MCP
3. Claude.ai fait un resume de l'etat actuel et propose la suite

### Session UnrealClaude (editeur)
1. Ouvrir Tools -> Claude Assistant -> NOUVELLE session
2. Commencer par : "CONTEXTE : Tu es l'assistant UnrealClaude lance dans UE5.7 depuis 'Tools => Claude Assistant', tu as acces a 28 MCP Tools."
3. Agent en mode DISCOVERY UNIQUEMENT -- pas de blueprint_modify

---

*Derniere mise a jour : 18/05/2026*
