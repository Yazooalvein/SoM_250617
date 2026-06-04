# BP_InventoryComponent -- Snapshot

**Path UE5 :** `/Game/Systems/Inventory/BP_InventoryComponent`
**Parent :** ActorComponent
**Noeuds totaux :** 16
**Dernier snapshot :** 05/06/2026 -- Audit global

---

## Variables

| Nom | Type | Notes |
|---|---|---|
| DiscoveredWeapons | TArray<FName> | Valeurs par defaut via Details panel instance HC -- dette BeginPlay C2 |

## Fonctions

| Nom | Inputs | Outputs | Notes |
|---|---|---|---|
| AddWeapon | WeaponID:FName | -- | Ajoute a DiscoveredWeapons |
| GetWeapons | -- | TArray<FName> | Retourne DiscoveredWeapons |

## Dependances

**Appelle :** --
**Appele par :** BP_SoM_HeroCharacter (EquipWeapon -> AddWeapon), UI_Radial_Main (GetWeapons pour slots)
**BPI_Saveable :** oui -- DiscoveredWeapons sauvegarde/charge

## Dettes actives

- Valeurs par defaut via Details panel HC -> migrer vers BeginPlay C2
- Accueillera a terme : consommables Seiken, materiaux craft, equipement
