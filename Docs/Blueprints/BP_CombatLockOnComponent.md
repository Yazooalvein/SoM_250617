# BP_CombatLockOnComponent -- Snapshot

**Role** : Gestion complete du systeme lock-on. Detecte, selectionne, maintient et desactive le ciblage d'un ennemi.
**Path UE5** : /Game/Systems/LockOn/BP_CombatLockOnComponent
**Type** : ActorComponent Blueprint
**Jalon** : COMBAT-LockOnRefacto (08/06/2026)

---

## Variables

| Nom | Type | Notes |
|---|---|---|
| bisLockOnActive | bool | true = lock actif |
| CurrentTarget | Actor ref | Cible actuellement lockee (null si inactif) |
| AvailableTargets | Array<Actor> | Liste des cibles valides dans le rayon |
| LockOnRange | float | Rayon de detection et de maintien |
| SwitchCooldown | float | Delai entre deux switches de cible |
| OnLockOnActivated | Dispatcher | Notifie quand le lock s'active |
| OnLockOnDeactivated | Dispatcher | Notifie quand le lock se desactive |

---

## Fonctions

| Nom | Inputs | Outputs | Notes |
|---|---|---|---|
| ActivateLockOn | - | - | DetectAvailableTargets -> SelectInitialTarget -> Branch IsValid(CurrentTarget) -> SET bisLockOnActive=true -> DoesImplementInterface check -> Call OnLockOnActivated |
| DeactivateLockOn | - | - | SET bisLockOnActive=false -> IsValid(CurrentTarget) -> Call OnLockOnDeactivated -> SET CurrentTarget=null |
| DetectAvailableTargets | - | - | Clear AvailableTargets -> SphereOverlap(Pawn) -> ForEachLoop -> DoesImplementInterface(BPI_Lockable) -> Message IsDeadOrDestroyed -> Branch(NOT bIsDead) -> Array_Add |
| SelectInitialTarget | - | - | Branch(Length > 0) -> ForEachLoop -> Message IsDeadOrDestroyed -> AND(IsValid, NOT bIsDead) -> update BestTarget par distance -> SET CurrentTarget=BestTarget |
| SwitchLockOnTarget | Direction : float | - | Trouve la prochaine cible dans la direction (gauche/droite) avec SwitchCooldown |
| HandleTargetDeath | - | - | CurrentTarget mort -> DetectAvailableTargets -> si cibles disponibles : SelectInitialTarget, sinon : DeactivateLockOn |
| GetCurrentLockOnTarget | - | CurrentTarget : Actor | Getter pure |

---

## Event Tick

```
bisLockOnActive AND IsValid(CurrentTarget)
  -> VSize(GetOwner.Location - CurrentTarget.Location) > LockOnRange
      -> True : DeactivateLockOn
```

---

## Dependances

- **Utilise** : BPI_Lockable (DoesImplementInterface + Message IsDeadOrDestroyed + Message OnLockableTargetDied)
- **Dispatchers ecoutes par** : BP_Enemy_Base (OnLockOnActivated -> OnSelfLocked, OnLockOnDeactivated -> OnSelfUnlocked)
- **Appele par** : BP_SoM_PlayerController (via GetBP_CombatLockOnComponent accessor)
- **Sur** : BP_SoM_HeroCharacter

---

## Gotchas

- GetComponentByClass(BP_CombatLockOnComponent) -> cible = GetPlayerCharacter(0), PAS GetPlayerController(0)
- SelectInitialTarget : bIsDead output -> NOT Boolean -> AND.B (filtre vivants uniquement)
- HandleTargetDeath NE DOIT PAS etre appele depuis SelectInitialTarget directement -- uniquement depuis OnLockableTargetDied callback
- DebugPrintVar presente dans DetectAvailableTargets -- a supprimer avant MAP-C1Level

---

## Dettes actives

- OnLockableTargetDied binding -> HandleTargetDeath : implementer proprement (actuellement non branche)
- DebugPrintVar a supprimer avant MAP-C1Level

---

*Dernier snapshot : 08/06/2026 -- COMBAT-LockOnRefacto*
