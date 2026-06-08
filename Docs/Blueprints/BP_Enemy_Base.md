# BP_Enemy_Base -- Snapshot

**Role** : Classe de base pour tous les ennemis. Gere les stats, le comportement de mort, les drops, le lock-on et la barre de vie.
**Path UE5** : /Game/Characters/Enemies/Blueprints/BP_Enemy_Base
**Type** : Character Blueprint
**Jalon** : COMBAT-LockOnRefacto (08/06/2026)

---

## Interfaces implementees

| Interface | Fonctions implementees |
|---|---|
| BPI_Lockable | GetLockSocketName (retourne "HeadLock"), IsDeadOrDestroyed (bIsDead OR IsActorBeingDestroyed), OnLockableTargetDied (appele depuis KillMeNow) |

---

## Variables

| Nom | Type | Notes |
|---|---|---|
| bIsDead | bool | true apres KillMeNow |
| bIsLocked | bool | true quand cible lockee par le hero |
| bForceHealthBarVisible | bool | Force affichage barre HP independamment du lock |
| EnemyHealthBarRef | UI_Enemy_HealthBar ref | Widget barre de vie |
| SkeletalMesh | SkeletalMeshComponent | Mesh de l'ennemi (utilise pour GetSocketLocation) |
| WeaponClass | BP_Enemy_Sword01_C* | Dette : hardcode, migrer vers DT_Enemy C2 |

---

## Fonctions / Events

| Nom | Type | Notes |
|---|---|---|
| KillMeNow | Custom Event | SET bIsDead=true -> Call OnLockableTargetDied -> flux mort (OnDeath dispatcher, spawn EssenceOrb) |
| OnSelfLocked | Custom Event | Bind sur OnLockOnActivated. GetPlayerCharacter -> Cast HC -> GetComponentByClass(BP_CombatLockOnComponent) -> GetCurrentLockOnTarget == Self -> SET bIsLocked=true -> UpdateHealthBarVisibility |
| OnSelfUnlocked | Custom Event | Bind sur OnLockOnDeactivated. SET bIsLocked=false -> UpdateHealthBarVisibility |
| UpdateHealthBarVisibility | Custom Event | Branch(bIsLocked OR bForceHealthBarVisible) -> SetVisibility(Visible / Hidden) sur EnemyHealthBarRef |
| EnableWeaponCollision | Function | Active collision arme |
| DisableWeaponCollision | Function | Desactive collision arme |
| TriggerHitFlash | Function | ABANDONNE -- presente mais ne sert a rien |

---

## BeginPlay

```
GetPlayerCharacter(0) -> GetComponentByClass(BP_CombatLockOnComponent) -> IsValid
  -> Bind OnLockOnActivated -> OnSelfLocked
  -> Bind OnLockOnDeactivated -> OnSelfUnlocked
```

---

## Flux mort (KillMeNow)

```
SET bIsDead=true
-> Call OnLockableTargetDied (BPI_Lockable)
-> Call OnDeath dispatcher
-> SpawnActor(BP_EssenceOrb, GetActorLocation) -> SET EssenceDropValue=15
-> RandomFloat > 0.5 -> SpawnActor(BP_ItemDrop) [stub C1]
```

---

## Dependances

- **Implemente** : BPI_Lockable
- **Ecoute dispatchers** : BP_CombatLockOnComponent.OnLockOnActivated, OnLockOnDeactivated
- **Spawne** : BP_EssenceOrb (mort), BP_ItemDrop (chance)
- **Reference** : BP_SoM_PlayerController via GetPlayerController (pour InputMode lors interactions futures)

---

## Dettes actives

- WeaponClass hardcode BP_Enemy_Sword01_C* -> migrer vers DT_Enemy en C2
- TriggerHitFlash : dead code, Hit Flash ABANDONNE -> nettoyage C2
- EssenceDropValue hardcode 15 -> DT_Enemy C2
- ItemDropChance hardcode 0.5 -> DT_Item C2
- DebugPrintVar a supprimer avant MAP-C1Level
- Stats ennemis (HP, ATK...) -> ENEMY-Base C1

---

## Anomalies connues

- TriggerHitFlash presente malgre Hit Flash ABANDONNE (anomalie #5 audit 05/06/2026)

---

*Dernier snapshot : 08/06/2026 -- COMBAT-LockOnRefacto*
