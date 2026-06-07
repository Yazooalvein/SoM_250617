# UI_FountainMenu -- Snapshot

**Path UE5 :** `/Game/UI/Widgets/FountainMenu/UI_FountainMenu`
**Parent :** UserWidget
**Noeuds totaux :** 28 (EventGraph)
**Dernier snapshot :** 07/06/2026 -- UI-FountainMenu

---

## Variables

Aucune variable Blueprint declaree.

## Widgets

| Widget | Type | Notes |
|---|---|---|
| Btn_SeReposer | Button | Bouton principal repos |
| Btn_MenuInventaire | Button | Bouton inventaire (stub WIP C1) |

## EventGraph -- Boutons

### Btn_SeReposer -- OnClicked
1. PrintString "Se Reposer : Regen + Save" (debug -- dette a supprimer)
2. GetGameMode -> Cast to BP_SoM_GameMode -> **OnFountainRest(FountainID=None)** ⚠️ FountainID hardcode None
3. RemoveFromParent (ferme le menu)
4. GetOwningPlayer -> Cast to BP_SoM_PlayerController
5. Set bShowMouseCursor = false
6. SetInputModeGameOnly
7. GetSubsystem(EnhancedInput) -> RemoveMappingContext(IMC_Menu) + AddMappingContext(IMC_Gameplay, priority=0)

> **Dettes actives :**
> - FountainID hardcode None -> passer via variable widget C2
> - PurgeCorruption absent de ce flow -> corriger avant ENEMY-Base
> - Respawn ennemis absent (stub) -> MAP-C1Level

### Btn_MenuInventaire -- OnClicked
1. PrintString "Menu Inventaire : WIP" (debug)
2. RemoveFromParent
3. GetOwningPlayer -> Cast to BP_SoM_PlayerController
4. Set bShowMouseCursor = false
5. SetInputModeGameOnly
6. GetSubsystem(EnhancedInput) -> RemoveMappingContext(IMC_Menu) + AddMappingContext(IMC_Gameplay, priority=0)

> Stub complet -- aucune logique inventaire. Jalon dedie C2.

## Ouverture du menu (depuis BP_FountainComponent.OnPlayerInteract)

1. GetPlayerController -> Cast to BP_SoM_PlayerController
2. CreateWidget(UI_FountainMenu) + AddToViewport
3. Set bShowMouseCursor = true
4. SetInputModeUIOnly
5. RemoveMappingContext(IMC_Gameplay) + AddMappingContext(IMC_Menu, priority=1)

## Dependances

**Appelle :** BP_SoM_GameMode.OnFountainRest
**Cree par :** BP_FountainComponent.OnPlayerInteract
**Appele par :** BP_FountainComponent (via CreateWidget)

## Notes techniques

- Pas de variable FountainID dans le widget -- OnFountainRest recu avec None (dette confirmee)
- SetInputModeGameOnly sur les deux boutons assure le retour propre au gameplay
- IMC_Menu priority=1 a l'ouverture, IMC_Gameplay priority=0 a la fermeture -- ordre correct
