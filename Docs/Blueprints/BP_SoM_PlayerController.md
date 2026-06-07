# BP_SoM_PlayerController -- Snapshot

**Path UE5 :** `/Game/Characters/Players/Blueprint/BP_SoM_PlayerController`
**Parent :** PlayerController
**Noeuds totaux :** 410 (EventGraph 217 + fonctions)
**Dernier snapshot :** 07/06/2026 -- UI-FountainMenu

---

## Variables

| Nom | Type | Categorie | Notes |
|---|---|---|---|
| PlayerCharacterRef | BP_SoM_HeroCharacter_C* | Default | SET dans OnPossess |
| RadialMainRef | UI_Radial_Main_C* | Default | |
| LockOnIndicatorWidgetRef | UI_LockOnIndicator_C* | UI\|LockOn | |
| QuickslotUp | FName | Default | Slot sort haut |
| QuickslotLeft | FName | Default | Slot sort gauche |
| QuickslotRight | FName | Default | Slot sort droit |
| bPlayerIsLooking | bool | Default | |
| LookIdleTime | double | Default | |
| LookReturnDelay | double | Default | |
| LockOnReturnSpeed | double | Default | |
| bSwitchInProgress | bool | UI\|LockOn | Guard anti-double SwitchTarget |
| LastLockOnSwitchTime | double | UI\|LockOn | |
| LockOnPitchMin | double | UI\|LockOn | |
| LockOnPitchMax | double | UI\|LockOn | |

## Fonctions

| Nom | Inputs | Outputs | Notes |
|---|---|---|---|
| InitializeSystems | -- | -- | GetControlledPawn -> Cast HC -> InitInputMapping -> Bind LockOnActivated/Deactivated. Contient DebugPrintVar (dette) |
| InitInputMapping | -- | -- | Add IMC_Gameplay via EnhancedInputSubsystem |
| GetBP_CombatLockOnComponent | -- | BP_CombatLockOnComponent_C* | Helper lookup par GetComponentByClass |
| GetCurrentLockOnTarget | -- | Actor* | Wrapper sur LockOnComponent.CurrentTarget |
| ToggleRadial | -- | -- | |
| OpenRadial | -- | -- | |
| CloseRadial | -- | -- | |
| Handle_UI_Radial_Rotate | AxisValue:double | -- | |
| ValidateRadial | -- | -- | |
| UpdateLockOnRotation | -- | -- | Appele dans Tick |
| UpdateLockOnUIIndicator | -- | -- | Appele dans Tick |
| Aim | AxisX:float, AxisY:double | -- | IA_Look gere dans PC (pas HC) -- regle permanente |

## EventGraph -- Events

| Event | Source | Comportement |
|---|---|---|
| Event OnPossess | Engine | Cast HC -> InitializeSystems -> Bind OnPlayerDeath -> Bind OnDestroyed -> AddMappingContext(IMC_Gameplay) |
| On Pawn Destroyed (Custom Event) | Bind OnDestroyed | Find PlayerStart -> Spawn BP_SoM_HeroCharacter -> Possess |
| OnHeroDied (Custom Event) | Bind OnPlayerDeath sur HC | Loge reponse mort hero (EssenceDrop + respawn) |
| Event Tick | Engine | Branch(bisLockOnActive && IsValid(IndicatorRef)) -> UpdateLockOnRotation -> UpdateLockOnUIIndicator |
| ShowLockOnIndicator (Custom Event) | LockOnComponent | IsValid? -> RemoveFromParent puis CreateWidget(UI_LockOnIndicator) -> AddToViewport(Z=10) -> SET LockOnIndicatorWidgetRef |
| HideLockOnIndicator (Custom Event) | LockOnComponent | IsValid? -> RemoveFromParent |

## EventGraph -- Inputs

| Input Action | Trigger | Comportement |
|---|---|---|
| IA_LockOn | Triggered | GetControlledPawn -> Cast HC -> GetComponentByClass(LockOn) -> Branch(bisLockOnActive) -> Activate / Deactivate |
| IA_SwitchTarget | Triggered | IsValid(IndicatorRef) && !bSwitchInProgress && Abs(AxisValue) > 0.5 -> GetLockOnComponent -> SwitchLockOnTarget(direction) -> SET bSwitchInProgress true/false |
| IA_UI_Radial_Open | Triggered | ToggleRadial |
| IA_UI_Radial_Rotate | Triggered | HandleUIRadialRotate(AxisValue) |
| IA_UI_Radial_Validate | Triggered | ValidateRadial (avec Branch) |
| IA_Interact | Triggered | GetOverlappingActors(HC) -> ForEachLoop -> DoesImplementInterface(BPI_Interactable) -> Message Interact(Target=Element, Instigator=Self) |
| IA_inflictdamage | Started | GetCurrentLockOnTarget -> ApplyDamage(5.0) -- DEBUG UNIQUEMENT |

## Dependances

**Appelle :** BP_SoM_HeroCharacter, BP_CombatLockOnComponent, UI_Radial_Main, UI_LockOnIndicator, BP_SoM_GameMode, BPI_Interactable
**Appele par :** GameMode (PlayerControllerClass), auto-possede le Pawn

## Notes techniques

- IA_Look gere dans PC (pas dans HC) -- regle permanente
- UpdateLockOnRotation V2 : bPlayerIsLooking + LookReturnDelay + LockOnReturnSpeed
- InitializeSystems : contient encore DebugPrintVar (dette -- supprimer avant MAP-C1Level)
- IA_Interact : utilise GetOverlappingActors(HC) + DoesImplementInterface -- NE PAS caster sur types concrets
- OnPossess remplace BeginPlay pour l'init (le PC peut reposseder un pawn apres mort)
- SwitchCooldown source unique : BP_CombatLockOnComponent (bSwitchInProgress dans PC = guard UI seul)
