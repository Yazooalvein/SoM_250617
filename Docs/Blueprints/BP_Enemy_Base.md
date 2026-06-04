# BP_Enemy_Base -- Snapshot

**Path UE5 :** `/Game/Characters/Enemies/Blueprints/BP_Enemy_Base`
**Parent :** Character
**Noeuds totaux :** 154
**Dernier snapshot :** 05/06/2026 -- Audit global

---

## Variables

| Nom | Type | Notes |
|---|---|---|
| bIsValid | bool | |
| bCanBeLocked | bool | Eligible lock-on |
| bIsDead | bool | |
| bIsLocked | bool | |
| bIsAttacking | bool | |
| bHasAlreadyHit | bool | Anti-multi-hit |
| bForceHealthBarVisible | bool | |
| OnDeath | Dispatcher | Point d'accroche ENEMY-DropSystem |
| MaxHealth / CurrentHealth | double | ⚠️ pas sur BP_AttributeSet -- dette ENEMY-Base |
| EnemyHealthBarRef | UI_Enemy_HealthBar_C* | |
| HealthBarFadeDelay | double | |
| FadeTimerHandle | TimerHandle | |
| AttackRadius | double | |
| WeaponClass | BP_Enemy_Sword01_C* | ⚠️ hardcode -- dette ENEMY-Types C2 |
| SpawnedWeapon | BP_Enemy_Sword01_C* | |
| HitFlashDMIs | TArray<MaterialInstanceDynamic*> | |
| As_BP_AIController | ref | Variable Cast stockee |
| As_BP_SoM_HeroCharacter | ref | Variable Cast stockee |

## Fonctions

| Nom | Inputs | Outputs | Notes |
|---|---|---|---|
| EquipWeapon | -- | -- | Spawn arme physique |
| EnableWeaponCollision | -- | -- | |
| DisableWeaponCollision | -- | -- | |
| TriggerHitFlash | ScalarValue:double | -- | ⚠️ present malgre Hit Flash ABANDONNE -- code mort |
| OnHealthBarFadeTimerExpired | -- | -- | |

## Dependances

**Appelle :** BP_Enemy_Sword01 (hardcode), UI_Enemy_HealthBar, BP_AIController_Enemy_Base
**Appele par :** BP_Enemy_Knight (heritage), BP_AIController_Enemy_Base
**BPI_TakeDamage :** implemente

## Dettes actives

- `MaxHealth` / `CurrentHealth` pas sur BP_AttributeSet -> migrer ENEMY-Base C1
- `WeaponClass` hardcode BP_Enemy_Sword01_C* -> generaliser ENEMY-Types C2
- `TriggerHitFlash` code mort -> supprimer nettoyage C2

## Notes -- ENEMY-DropSystem (prochain jalon)

`OnDeath` dispatcher est le point d'accroche naturel pour spawner BP_EssenceDrop :
```
OnDeath -> SpawnActor(BP_EssenceDrop) -> SET EssenceValue -> (chance objet simple)
```
EssenceValue configurable par instance (expose en Instance Editable).
