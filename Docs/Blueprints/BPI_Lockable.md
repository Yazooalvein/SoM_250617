# BPI_Lockable -- Snapshot

**Role** : Interface de ciblage lock-on. Permet au BP_CombatLockOnComponent de cibler tout Actor sans connaitre son type concret.
**Path UE5** : /Game/Systems/BPI/BPI_Lockable
**Type** : Blueprint Interface
**Jalon creation** : COMBAT-LockOnRefacto (08/06/2026)

---

## Fonctions / Events

| Nom | Type | Inputs | Outputs | Notes |
|---|---|---|---|---|
| GetLockSocketName | Function | - | SocketName : FName | Retourne le nom du socket de ciblage (ex: "HeadLock"). Pure. |
| IsDeadOrDestroyed | Function | - | bIsDead : bool | Retourne (bIsDead OR IsActorBeingDestroyed). Pure. |
| OnLockableTargetDied | Event | - | - | Declenche quand l'ennemi meurt. Notifie le composant lock-on. |

---

## Implementeurs actuels

| Blueprint | Impl. GetLockSocketName | Impl. IsDeadOrDestroyed | Impl. OnLockableTargetDied |
|---|---|---|---|
| BP_Enemy_Base | Retourne "HeadLock" | bIsDead OR IsActorBeingDestroyed | Appele depuis flux mort KillMeNow |

---

## Dependances

- **Appele par** : BP_CombatLockOnComponent (DetectAvailableTargets, SelectInitialTarget, SwitchLockOnTarget, ActivateLockOn, UpdateLockOnUIIndicator dans PC)
- **Implemente par** : BP_Enemy_Base (C1). Futurs : boss, pieges lockables (C2+)

---

## Dettes actives

- **GetLockMesh() -> SceneComponent** : a ajouter en C2 pour eliminer le Cast BP_Enemy_Base dans UpdateLockOnUIIndicator du PC
- **OnLockableTargetDied -> HandleTargetDeath** : binding a implementer proprement (callback mort cible -> BP_CombatLockOnComponent.HandleTargetDeath)

---

## Gotchas

- Message IsDeadOrDestroyed : le pin `self` DOIT etre explicitement connecte a la cible. Si `bDefaultValueIsIgnored=True` sur le pin self, le noeud retourne toujours la valeur par defaut (false) sans appeler l'implementation.

---

*Dernier snapshot : 08/06/2026 -- COMBAT-LockOnRefacto*
