# BP_CombatLockOnComponent -- Snapshot

**Path UE5 :** `/Game/Systems/LockOn/BP_CombatLockOnComponent`
**Parent :** ActorComponent
**Noeuds totaux :** 275
**Dernier snapshot :** 05/06/2026 -- Audit global

---

## Variables

| Nom | Type | Categorie | Notes |
|---|---|---|---|
| bisLockOnActive | bool | LockOn\|Core | |
| CurrentTarget | Actor* | LockOn\|Core | |
| AvailableTargets | TArray<Actor*> | LockOn\|Core | |
| SwitchCooldown | double | LockOn\|Params | SOURCE UNIQUE -- jamais dans PC |
| LockOnRange | double | LockOn\|Params | |
| LastSwitchTime / SwitchTime | double | Runtime | |
| OwnerCharacter | BP_SoM_HeroCharacter_C* | Runtime | |
| TempAvailableTargets | TArray<Actor*> | Default | Buffer tri |
| SwitchTarget | Actor* | Default | |
| OnLockOnActivated / OnLockOnDeactivated | Dispatcher | Default | |
| LockOnInputAction / SwitchInputAction | FName | LockOn\|Input | |

## Fonctions

| Nom | Inputs | Outputs | Notes |
|---|---|---|---|
| ActivateLockOn | -- | -- | |
| DeactivateLockOn | -- | -- | |
| SwitchLockOnTarget | Direction:double | -- | |
| DetectAvailableTargets | -- | -- | |
| SelectInitialTarget | -- | -- | |
| GetCurrentLockOnTarget | -- | Actor* | |
| IsLockOnActive | -- | bool | |
| IsSwitchTargetValid | Target, CurrentTarget, ActorLoc, PlayerLoc, PlayerRight, PlayerFwd, SwitchDir, MinAngle | bool+double+double | |

## Dependances

**Appelle :** BP_Enemy_Base (tag/detection)
**Appele par :** BP_SoM_PlayerController, BP_ComboManagerComponent

## Notes techniques

- SwitchCooldown = SOURCE UNIQUE -- jamais creer LockOnSwitchCooldown dans le PC
- Rotation Rate Z = -1 sur HC pour pivot instantane hors lock-on
