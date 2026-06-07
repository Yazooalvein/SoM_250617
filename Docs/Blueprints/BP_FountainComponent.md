# BP_FountainComponent -- Snapshot

**Path UE5 :** `/Game/Systems/Save/BP_FountainComponent`
**Parent :** ActorComponent
**Interfaces :** BPI_Saveable, BPI_Interactable (via BP_Fountain_Actor)
**Dernier snapshot :** 07/06/2026 -- UI-FountainMenu

---

## Variables

| Nom | Type | Notes |
|---|---|---|
| FountainID | FName | Identifiant unique -- renseigner dans Details panel de chaque instance niveau |
| bIsActivated | bool | false = jamais active, true = deja active au moins une fois |

## Fonctions

| Nom | Inputs | Outputs | Notes |
|---|---|---|---|
| OnPlayerInteract | -- | -- | Point d'entree unique -- appele via BPI_Interactable.Interact sur BP_Fountain_Actor |
| SaveData | SaveGame (BP_SaveGame_SoM) | -- | BPI_Saveable : Array_Add(FountainID) dans SaveGame.ActivatedFountains |
| LoadData | SaveGame (BP_SaveGame_SoM) | -- | BPI_Saveable : Array_Contains(FountainID) -> SET bIsActivated |

## Logique OnPlayerInteract

```
Branch(bIsActivated)
  False (1ere activation) :
    SET bIsActivated = true
    GetOwner -> Cast BP_Fountain_Actor -> FountainLight -> SetIntensity(2000) + SetLightColor(chaud)
    GetPlayerController -> Cast PC -> GetGameMode -> Cast GameMode -> OnFountainRest(FountainID)
  True (interactions suivantes) :
    GetPlayerController -> Cast PC
    CreateWidget(UI_FountainMenu, OwningPlayer=PC) -> AddToViewport
    GetSubsystem(EnhancedInputLocalPlayerSubsystem) -> RemoveIMC(IMC_Gameplay) -> AddIMC(IMC_Menu)
    SetShowMouseCursor(true) -> SetInputModeUIOnly
```

## Dependances

**Appelle :** BP_SoM_GameMode.OnFountainRest, BP_Fountain_Actor.FountainLight, UI_FountainMenu
**Appele par :** BP_Fountain_Actor.Interact (via BPI_Interactable)
**Contenu dans :** BP_Fountain_Actor

## Dettes actives

- FountainID hardcode None dans UI_FountainMenu.Se reposer -> passer via variable widget C2
- Se reposer : PurgeCorruption non branche -> corriger avant ENEMY-Base
- Se reposer : respawn ennemis stub -> MAP-C1Level
