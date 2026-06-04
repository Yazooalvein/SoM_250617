# BP_Fountain_Actor -- Snapshot

**Path UE5 :** `/Game/Systems/Save/BP_Fountain_Actor`
**Parent :** Actor
**Noeuds totaux :** 6
**Dernier snapshot :** 05/06/2026 -- Audit global

---

## Composants

Definis dans UserConstructionScript (non listes par MCP).

## EventGraph

3 events dont : interaction joueur -> BP_FountainComponent.OnPlayerInteract

## Dependances

**Contient :** BP_FountainComponent
**Appelle :** BP_FountainComponent.OnPlayerInteract

## Notes -- jalon UI-FountainMenu

C'est l'Actor place dans le niveau. La logique metier est dans BP_FountainComponent.
Pour UI-FountainMenu : l'interaction joueur doit brancher sur la logique bIsActivated avant d'appeler OnFountainRest.
