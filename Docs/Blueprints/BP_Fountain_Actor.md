# BP_Fountain_Actor -- Snapshot

**Path UE5 :** `/Game/Systems/Save/BP_Fountain_Actor`
**Parent :** Actor
**Noeuds totaux :** 28 (EventGraph)
**Dernier snapshot :** 07/06/2026 -- UI-FountainMenu

---

## Composants

| Composant | Type | Notes |
|---|---|---|
| PointLight | PointLightComponent | Feedback visuel proximite + activation |
| (Mesh, Collision) | Definis dans UserConstructionScript | Non listes par MCP |

## Variables

| Nom | Type | Valeur defaut | Notes |
|---|---|---|---|
| bPlayerInRange | bool | false | Track presence joueur dans la sphere |

> Note : FountainID est sur BP_FountainComponent, PAS sur cet Actor.

## Interfaces implementees

- **BPI_Interactable** : Event Interact(Instigator: BP_SoM_PlayerController_C*)

## EventGraph -- Events

### Event BeginPlay
- Deconnecte (then=0). Aucune logique au BeginPlay.

### Event ActorBeginOverlap
1. Cast to BP_SoM_HeroCharacter (si echec : ignore)
2. Set bPlayerInRange = true
3. GetComponentByClass(BP_FountainComponent)
4. Get bIsActivated -> Branch
   - **TRUE** (deja activee) : Set Intensity **2000** + Set Color **orange chaud** `(R=1.0, G=0.625, B=0.0)`
   - **FALSE** (pas encore activee) : Set Intensity **500** + Set Color **bleu** `(R=0.3, G=0.5, B=1.0)`

### Event ActorEndOverlap
1. Cast to BP_SoM_HeroCharacter (si echec : ignore)
2. Set bPlayerInRange = false
3. Set Intensity **500** + Set Color **bleu** `(R=0.3, G=0.5, B=1.0)`

### Event Tick
- Deconnecte (then=0). Dead code : contient un GetComponentByClass -> OnPlayerInteract orphelin.

### Event Interact (From BPI_Interactable)
1. GetComponentByClass(BP_FountainComponent)
2. Call OnPlayerInteract (sur FountainComponent)

## Dependances

**Contient :** BP_FountainComponent (GetComponentByClass)
**Implemente :** BPI_Interactable
**Appelle :** BP_FountainComponent.OnPlayerInteract
**Appele par :** BP_SoM_PlayerController (via BPI_Interactable message)

## Notes techniques

- FountainID : sur BP_FountainComponent, pas sur cet Actor -- renseigner dans le Details panel de l'instance FountainComponent
- PointLight colors : bleu = inactive/idle, orange = activee (repos possible)
- Tick dead code a nettoyer (GetComponentByClass orphelin) -- faible priorite
- La logique metier (bIsActivated, save, UI) est entierement dans BP_FountainComponent
