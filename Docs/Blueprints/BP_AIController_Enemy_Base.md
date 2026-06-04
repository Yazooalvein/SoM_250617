# BP_AIController_Enemy_Base -- Snapshot

**Path UE5 :** `/Game/IA/Controllers/BP_AIController_Enemy_Base`
**Parent :** AIController
**Noeuds totaux :** 52
**Dernier snapshot :** 05/06/2026 -- Audit global

---

## Variables

| Nom | Type | Notes |
|---|---|---|
| CurrentTarget | Actor* | |
| ControlledEnemy | BP_Enemy_Base_C* | |
| HasAggro / TargetActor / HomeLocation | FName | Cles Blackboard |
| AggroRadius / AttackRadius / LoseAggroRadius | double | |
| LoseAggroDelay | double | |
| LoseAggroTimerHandle | TimerHandle | |
| HomeLoc | Vector | Position de repos |
| TargetNone | Object* | Valeur null BB |

## Fonctions

| Nom | Inputs | Outputs | Notes |
|---|---|---|---|
| InitBlackboardKeys | Pawn:Actor* | -- | Initialise les cles BB |
| ClearTarget | -- | -- | |

## Dependances

**Appelle :** BP_Enemy_Base (ControlledEnemy)
**Utilise :** BehaviorTree BB -- HasAggro, TargetActor, HomeLocation
