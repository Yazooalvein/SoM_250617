# BP_Enemy_Base -- Snapshot

**Path UE5 :** `/Game/Characters/Enemies/Blueprints/BP_Enemy_Base`
**Parent :** Character
**Dernier snapshot :** 06/06/2026 -- ENEMY-DropSystem

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
| OnDeath | Dispatcher | Point d'accroche drops |
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

| Nom | Notes |
|---|---|
| EquipWeapon | Spawn arme physique |
| EnableWeaponCollision | |
| DisableWeaponCollision | |
| KillMeNow | Custom Event : SET bIsDead=true -> Call OnDeath -> spawn drops -> destroy |
| TriggerHitFlash | ⚠️ code mort -- Hit Flash ABANDONNE |
| OnHealthBarFadeTimerExpired | |

## Flow OnDeath (ENEMY-DropSystem)

```
KillMeNow -> SET bIsDead=true -> Call OnDeath
  -> SpawnActor(BP_EssenceOrb, GetActorLocation) -> SET EssenceDropValue=15 (hardcode C1)
  -> DestroyActor(self) + DestroyActor(SpawnedWeapon)
  -> RandomFloatInRange(0,1) > 0.5 -> Branch true : SpawnActor(BP_ItemDrop) [stub C1]
```

## Dependances

**Appelle :** BP_Enemy_Sword01 (hardcode), UI_Enemy_HealthBar, BP_AIController_Enemy_Base, BP_EssenceOrb
**Appele par :** BP_Enemy_Knight (heritage), BP_AIController_Enemy_Base
**BPI_TakeDamage :** implemente

## Dettes actives

- `MaxHealth` / `CurrentHealth` pas sur BP_AttributeSet -> migrer ENEMY-Base C1
- `WeaponClass` hardcode BP_Enemy_Sword01_C* -> generaliser ENEMY-Types C2
- `TriggerHitFlash` code mort -> supprimer nettoyage C2
- EssenceDropValue hardcode 15 -> DT_Enemy C2
- ItemDropChance hardcode 0.5 -> DT_Item C2
- BP_ItemDrop stub (overlap -> DestroyActor) -> brancher InventoryComponent C2
- DebugPrintVar a supprimer avant MAP-C1Level
