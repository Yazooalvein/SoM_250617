# BP_SoM_HeroCharacter -- Snapshot

**Path UE5 :** `/Game/Characters/Players/Blueprint/BP_SoM_HeroCharacter`
**Parent :** Character (Blueprint Only)
**Noeuds totaux :** 395
**Dernier snapshot :** 05/06/2026 -- Audit global

---

## Variables

| Nom | Type | Categorie | Notes |
|---|---|---|---|
| AttributeSetRef | BP_AttributeSet_Base_C* | Stats\|Principals | Reference principale stats |
| StatsDataTable | DataTable* | Stats\|Principals | DT source init stats |
| CurrentWeapon | BP_Weapon_Base_C* | Weapons | Arme physique spawnee |
| bIsDead | bool | Default | |
| bIsInvincible | bool | Default | |
| OnPlayerDeath | Dispatcher | Default | Binde par PC.BeginPlay |
| LastAxisX / LastAxisY | double | Default | Dernier input mouvement |
| bRadialUnlocked | bool | Default | ⚠️ espace trailing dans le nom -- attention FName |
| DashMontage | AnimMontage* | Dash | |
| RollMontage | AnimMontage* | Dash | |
| Has Dashed / Has Rolled / Has Jumped | bool | Dash/Jump | Runtime flags |
| Is Dashing / Is Rolling | bool | Dash | Runtime flags |
| bIsGrounded | bool | Dash | |
| Wall Jump * (4 params) | double | Wall Jump | Params mecanique wall jump |
| Trail Color | LinearColor | Jump Trail | |

## Fonctions

| Nom | Inputs | Outputs | Notes |
|---|---|---|---|
| Add_Main_HUD | -- | -- | Cree + ajoute UI_HUD_Main |
| InitAttributesFromDatatable | -- | -- | Appelle AttributeSet.InitStats |
| EquipWeapon | RowName:FName | -- | Spawn BP + InventoryComp.AddWeapon + ComboManager.EquipWeapon |
| IsDead | -- | bool | Pure getter bIsDead |
| Move | AxisX:double, AxisY:double | -- | |
| Aim | AxisX:float, AxisY:double | -- | |

**EventGraph :** 11 events, 287 noeuds

## Composants

- CapsuleComponent (root)
- SkeletalMeshComponent (Mesh hero)
- SpringArmComponent
- CameraComponent
- BP_CombatLockOnComponent
- BP_ComboManagerComponent
- BP_MagicComponent
- BP_InventoryComponent
- BP_CorruptionComponent

## Dependances

**Appelle :** BP_AttributeSet_Base, BP_ComboManagerComponent, BP_InventoryComponent, UI_HUD_Main
**Appele par :** BP_SoM_PlayerController (BeginPlay Cast), BP_SoM_GameMode (OnHeroDied)

## Dettes actives

- `bRadialUnlocked` espace trailing -> corriger FName avant tout usage conditionnel
- `DiscoveredWeapons` par defaut via Details panel HC -> migrer vers BeginPlay C2
- `EquipWeapon` spawn physique = point d'entree unique OK
