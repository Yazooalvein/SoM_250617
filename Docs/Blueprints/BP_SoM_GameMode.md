# BP_SoM_GameMode -- Snapshot

**Path UE5 :** `/Game/Core/BP_SoM_GameMode`
**Parent :** GameModeBase
**Noeuds totaux :** 44
**Dernier snapshot :** 05/06/2026 -- Audit global

---

## Variables

| Nom | Type | Notes |
|---|---|---|
| CurrentSaveGame | BP_SaveGame_SoM_C* | Instance save en cours |
| CurrentSlotName | FString | Nom du slot |

## Fonctions

| Nom | Inputs | Notes |
|---|---|---|
| OnFountainRest | FountainID:FName | Point d'entree unique save/fontaine |
| CollectSaveData | FountainID:FName | Collecte donnees via BPI_Saveable (GetComponentsByInterface) |
| CollectFountainTransform | FountainID:FName | ⚠️ prend index 0 -- filtrage par FountainID -> C2 |
| WriteSaveAndApplyFountainEffects | -- | Ecrit slot + soigne HP/ST/MP via SetStatValue |

## Dependances

**Appelle :** BP_SaveGame_SoM, BPI_Saveable (GetComponentsByInterface), BP_AttributeSet_Base (SetStatValue)
**Appele par :** BP_FountainComponent.OnPlayerInteract, BP_SoM_PlayerController.OnHeroDied

## Dettes actives

- `CollectFountainTransform` prend index 0 -> filtrage par FountainID a faire C2
- `WriteSaveAndApplyFountainEffects` SET HP/ST/MP = doublon avec AttributeSet.LoadData -> nettoyage C2

## Notes techniques

- PlayerControllerClass = BP_SoM_PlayerController (regle permanente)
- OnFountainRest = UNIQUE point d'entree pour toute save -- ne jamais appeler SaveGameToSlot ailleurs
