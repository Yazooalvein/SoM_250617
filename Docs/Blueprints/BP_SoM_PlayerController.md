# BP_SoM_PlayerController -- Snapshot

**Role** : Controleur joueur. Gere les inputs, la camera lock-on, les interactions, l'UI et le flux mort/respawn.
**Path UE5** : /Game/Characters/Players/Blueprint/BP_SoM_PlayerController
**Type** : PlayerController Blueprint
**Jalon** : COMBAT-LockOnRefacto (08/06/2026)

---

## Variables

| Nom | Type | Notes |
|---|---|---|
| PlayerCharacterRef | BP_SoM_HeroCharacter ref | Set dans BeginPlay |
| LockOnIndicatorWidgetRef | UI_LockOnIndicator ref | Widget indicateur lock-on |
| LockOnPitchMin / LockOnPitchMax | float | Clamp pitch camera en lock-on |
| LockOnReturnSpeed | float | Vitesse retour camera vers cible |
| LookReturnDelay | float | Delai avant retour auto camera |
| LookIdleTime | float | Temps ecoule sans input camera |
| bPlayerIsLooking | bool | true si le joueur donne un input camera |
| bIsLockOnActive | bool | Miroir local de bisLockOnActive |
| LastFountainTransform | Transform | Position derniere fontaine activee pour respawn |

---

## Fonctions

| Nom | Notes |
|---|---|
| GetBP_CombatLockOnComponent | Accessor vers le composant lock-on sur le Hero |
| UpdateLockOnUIIndicator | GetBP_CombatLockOnComponent -> Message GetLockSocketName(CurrentTarget) -> GetSocketLocation -> ProjectWorldToScreen -> SetPositionInViewport. Branch(ProjectionOK) -> SetVisibility(Visible) / SetVisibility(Hidden) |
| UpdateLockOnRotation | GetBP_CombatLockOnComponent -> DoesImplementInterface(CurrentTarget, BPI_Lockable) -> True : RInterpTo + SetControlRotation. False : DeactivateLockOn |
| OnInteract | IA_Interact Triggered -> GetOverlappingActors(HC) -> ForEachLoop -> DoesImplementInterface(BPI_Interactable) -> Message Interact(Target=Element, Instigator=Self) |
| OnHeroDied | Flux mort/respawn complet (voir Architecture cle CLAUDE.md) |
| OnFountainRest (delegation) | Delegation vers GameMode.OnFountainRest |

---

## Inputs bindes

| IA | Evenement | Handler |
|---|---|---|
| IA_LockOn | Triggered | ActivateLockOn / DeactivateLockOn |
| IA_LockOnSwitch | Triggered | SwitchLockOnTarget |
| IA_Look | Triggered | UpdateLockOnRotation (en lock) + camera libre |
| IA_Interact | Triggered | OnInteract |
| IA_Attack | Triggered | ComboManager.HandleAttack |
| IA_Jump / Dodge / Sprint | Triggered | Actions mouvement |

---

## Dependances

- **Utilise** : BP_CombatLockOnComponent (via GetBP_CombatLockOnComponent)
- **Utilise** : BPI_Lockable (DoesImplementInterface + Message GetLockSocketName dans UpdateLockOnUIIndicator)
- **Utilise** : BPI_Interactable (DoesImplementInterface + Message Interact dans OnInteract)
- **Reference** : BP_SoM_HeroCharacter (PlayerCharacterRef)
- **Reference** : BP_SoM_GameMode (via GetGameMode)

---

## Dettes actives

- Cast BP_Enemy_Base dans UpdateLockOnUIIndicator pour GET SkeletalMesh : dernier cast concret residuel -> migrer vers BPI_Lockable.GetLockMesh() en C2
- DebugPrintVar dans InitializeSystems -> avant MAP-C1Level

---

## Anomalies connues

- InitializeSystems contient DebugPrintVar (anomalie #11 audit 05/06/2026)

---

*Dernier snapshot : 08/06/2026 -- COMBAT-LockOnRefacto*
