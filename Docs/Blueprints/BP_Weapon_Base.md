# BP_Weapon_Base -- Snapshot

**Path UE5 :** `/Game/Weapons/Blueprints/BP_Weapon_Base`
**Parent :** Actor
**Noeuds totaux :** 47
**Dernier snapshot :** 05/06/2026 -- Audit global

---

## Variables

| Nom | Type | Notes |
|---|---|---|
| WeaponData | FWeaponData | Donnees depuis DT_Weapons |
| OwnerCharacter | BP_SoM_HeroCharacter_C* | |
| bIsEquipped | bool | |
| bCanDealDamage | bool | |
| TouchedActors | TArray<Actor*> | Anti-multi-hit |

## Fonctions

| Nom | Inputs | Outputs | Notes |
|---|---|---|---|
| OnEquipped | -- | -- | |
| OnUnequipped | -- | -- | |
| EnableWeaponCollision | -- | -- | |
| DisableWeaponCollision | -- | -- | |
| TryDealDamage | OtherActor:Actor* | Damages:double, Instigator:Actor*, Weapon:Actor* | Appelle BPI_TakeDamage |

## Sous-classes

- **BP_Weapon_Sword** : variable unique `RowName (FName)` -- identifiant DT_Weapons
- **BP_Weapon_2HSword** : idem

## Dependances

**Appelle :** BPI_TakeDamage sur cible
**Spawn par :** BP_SoM_HeroCharacter.EquipWeapon
