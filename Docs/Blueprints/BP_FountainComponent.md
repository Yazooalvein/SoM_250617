# BP_FountainComponent -- Snapshot

**Path UE5 :** `/Game/Systems/Save/BP_FountainComponent`
**Parent :** ActorComponent
**Noeuds totaux :** 7
**Dernier snapshot :** 05/06/2026 -- Audit global

---

## Variables

| Nom | Type | Notes |
|---|---|---|
| FountainID | FName | Identifiant unique de la fontaine |
| bIsActivated | bool | false = 1ere activation, true = menu |

## Fonctions

| Nom | Inputs | Outputs | Notes |
|---|---|---|---|
| OnPlayerInteract | -- | -- | Appelle BP_SoM_GameMode.OnFountainRest(FountainID) |

## Dependances

**Appelle :** BP_SoM_GameMode.OnFountainRest
**Contenu dans :** BP_Fountain_Actor

## A implementer -- UI-FountainMenu (C1)

Logique cible apres refacto :
```
OnPlayerInteract :
  Branch(bIsActivated)
  False : SET bIsActivated=true -> ChangerMateriauActeur -> RegenStats -> GameMode.OnFountainRest
  True  : Ouvrir UI_FountainMenu
```

- UI_FountainMenu.Se reposer : regen HP/ST/MP + save + respawn ennemis + PurgeCorruption + restock
- UI_FountainMenu.Menu Inventaire : quickslots + upgrade magie/deites + level up hero (Essence)
- bIsActivated persiste via BP_SaveGame_SoM.ActivatedFountains (TArray<FName>)
- Visuel C1 : changement matiere/couleur sur bIsActivated (pas d'anim -- ART-Fontaine futur)
