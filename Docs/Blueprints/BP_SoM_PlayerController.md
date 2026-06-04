# BP_SoM_PlayerController -- Snapshot

**Path UE5 :** `/Game/Characters/Players/Blueprint/BP_SoM_PlayerController`
**Parent :** PlayerController
**Noeuds totaux :** 402
**Dernier snapshot :** 05/06/2026 -- Audit global

---

## Variables

| Nom | Type | Categorie | Notes |
|---|---|---|---|
| PlayerCharacterRef | BP_SoM_HeroCharacter_C* | Default | SET au BeginPlay |
| RadialMainRef | UI_Radial_Main_C* | Default | |
| LockOnIndicatorWidgetRef | UI_LockOnIndicator_C* | UI\|LockOn | |
| QuickslotUp / QuickslotLeft / QuickslotRight | FName | Default | Sorts assignes aux slots rapides |
| bPlayerIsLooking | bool | Default | |
| LookIdleTime / LookReturnDelay | double | Default | |
| LockOnReturnSpeed | double | Default | |
| bSwitchInProgress | bool | UI\|LockOn | |
| LastLockOnSwitchTime | double | UI\|LockOn | |
| LockOnPitchMin / LockOnPitchMax | double | UI\|LockOn | |

## Fonctions

| Nom | Inputs | Outputs | Notes |
|---|---|---|---|
| InitializeSystems | -- | -- | Appelle InitInputMapping + autres |
| InitInputMapping | -- | -- | Add IMC_Gameplay |
| GetBP_CombatLockOnComponent | -- | BP_CombatLockOnComponent_C* | Helper lookup |
| GetCurrentLockOnTarget | -- | Actor* | |
| ToggleRadial / OpenRadial / CloseRadial | -- | -- | Gestion UI radiale |
| Handle_UI_Radial_Rotate | AxisValue:double | -- | |
| ValidateRadial | -- | -- | |
| UpdateLockOnRotation | -- | -- | Ticked |
| UpdateLockOnUIIndicator | -- | -- | |
| Aim | AxisX:float, AxisY:double | -- | IA_Look dans PC (pas HC) |
| OnHeroDied | -- | -- | Binde sur OnPlayerDeath |

**EventGraph :** 6 events, 209 noeuds

## Dependances

**Appelle :** BP_SoM_HeroCharacter, BP_CombatLockOnComponent, UI_Radial_Main, BP_SoM_GameMode
**Appele par :** BeginPlay auto (GameMode)

## Notes techniques

- IA_Look gere dans PC (pas dans HC) -- regle permanente
- UpdateLockOnRotation V2 : bPlayerIsLooking + LookReturnDelay 1.5s + LockOnReturnSpeed 3.0
- OnHeroDied : SpawnActor(BP_EssenceDrop) -> SetStatValue(EssenceValue,0) -> CameraFade -> respawn
