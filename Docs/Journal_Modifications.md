# Journal des Modifications -- Shadow of Mana

## Objectif
Suivi precis de toutes les evolutions majeures du projet.

## Entrees

### 09/06/2026 -- COMBAT-LockOnRefacto -- VALIDE PIE

#### BP_CombatLockOnComponent + BP_Enemy_Base -- lock-on PIE complet
- SwitchLockOnTarget : suppression doublon K2Node_CallDelegate_2 (OnLockOnDeactivated x2)
- SwitchLockOnTarget : ajout K2Node_CallDelegate_3 (OnLockOnActivated) apres OnLockOnDeactivated
- SwitchLockOnTarget : reordonnancement -- OnLockOnDeactivated desormais AVANT Set CurrentTarget = BestTargetTemp
- BP_Enemy_Base.BeginPlay : OnSelfUnlocked bind sur OnLockOnDeactivated mis en serie avec OnSelfLocked dans branche .then (etait dans .else -> jamais execute)

#### Bugs resolus
- Bug 1 : doublon OnLockOnDeactivated dans SwitchLockOnTarget -> ancienne cible recevait OnSelfUnlocked x2, nouvelle jamais OnSelfLocked -> HP bar ne s'affichait pas au switch
- Bug 2 : OnLockOnDeactivated appele apres Set CurrentTarget -> l'ancienne cible recevait OnSelfUnlocked alors que CurrentTarget pointait deja sur la nouvelle -> HP bar ancienne cible ne disparaissait pas
- Bug 3 : OnSelfUnlocked bind dans .else de Branch(IsValid(LockOnComp)) -> jamais execute si le composant est valide -> HP bar ne disparaissait jamais a l'unlock ni au switch

#### Dettes restantes COMBAT-LockOnRefacto -> ENEMY-Base
- OnLockableTargetDied binding HandleTargetDeath : callback mort cible non implemente -> ENEMY-Base
- Cast BP_Enemy_Base dans UpdateLockOnUIIndicator pour SkeletalMesh -> migrer vers GetLockMesh() dans BPI_Lockable -> C2
- DebugPrintVar actifs dans BP_CombatLockOnComponent -> supprimer avant MAP-C1Level
- ObjectTypeQuery3 (PhysicsBody) dans DetectAvailableTargets -> peut rater des ennemis

#### Etat final
COMBAT-LockOnRefacto VALIDE PIE complet. Lock, switch, unlock, HP bars hide/show, plus d'erreurs pending kill.

---

### 08/06/2026 -- COMBAT-LockOnRefacto -- DEBUGGING (PIE en cours)

#### BPI_Lockable + BP_CombatLockOnComponent + BP_Enemy_Base -- refacto lock-on
- Creation BPI_Lockable (GetLockSocketName, IsDeadOrDestroyed, OnLockableTargetDied) -- Content/Systems/BPI/
- BP_CombatLockOnComponent : refacto complete (nettoyage code mort, DetectAvailableTargets via BPI_Lockable, SelectInitialTarget, SwitchLockOnTarget, ActivateLockOn, DeactivateLockOn, Tick distance)
- BP_Enemy_Base : implemente BPI_Lockable, BeginPlay bind OnLockOnActivated->OnSelfLocked + OnLockOnDeactivated->OnSelfUnlocked
- BP_SoM_PlayerController : UpdateLockOnUIIndicator via Message GetLockSocketName, UpdateLockOnRotation via DoesImplementInterface

#### Bugs resolus pendant la session
- Bug 1 : GetComponentByClass(BP_CombatLockOnComponent) appele sur GetPlayerController au lieu de GetPlayerCharacter -> Accessed None -> correction GetPlayerCharacter(0)
- Bug 2 : SelectInitialTarget -- bIsDead non inverse dans AND Boolean -> ennemi mort selectionnable, vivant ignore -> insertion NOT Boolean
- Bug 3 : HandleTargetDeath appele inconditionnellement apres ForEachLoop.Completed dans SelectInitialTarget -> infinite loop -> suppression appel inconditionnel
- Diagnostic bugs 2+3 par audit agent UnrealClaude (blueprint_query, 67+142 noeuds analyses)

#### Dettes restantes COMBAT-LockOnRefacto
- OnLockableTargetDied binding HandleTargetDeath : a implementer proprement (callback mort cible, actuellement non branche)
- Cast BP_Enemy_Base dans UpdateLockOnUIIndicator pour GET SkeletalMesh : reste en C1, migrer vers GetLockMesh() dans BPI_Lockable en C2
- DebugPrintVar a supprimer dans BP_CombatLockOnComponent avant MAP-C1Level

#### Etat final
COMBAT-LockOnRefacto : lock-on refonctionne en PIE apres Fix 2+3. Checklist PIE complete en cours dans session suivante.

---

### 07/06/2026 -- UI-FountainMenu -- VALIDE PIE

#### Architecture interaction -- BPI_Interactable
- Creation de BPI_Interactable (Interact(Instigator: BP_SoM_PlayerController)) -- Content/Systems/
- PC.OnInteract : GetOverlappingActors(HC) -> ForEachLoop -> DoesImplementInterface(BPI_Interactable) -> Message Interact(Target=ArrayElement, Instigator=Self)
- Architecture extensible : vendeurs, PNJ, leviers implementeront BPI_Interactable en C2/C3 sans modifier le PC
- BP_Fountain_Actor implemente BPI_Interactable -- Interact() -> GetComponentByClass(BP_FountainComponent) -> OnPlayerInteract

#### IA_Interact -- nouvel input
- Creation IA_Interact (Digital/bool) dans Content/Input/InputActions/
- Ajout dans IMC_Gameplay : touche E (clavier) + Gamepad Face Button Bottom

#### BP_Fountain_Actor -- refacto
- InteractionZone : remplacement StaticMesh sphere par SphereComponent (radius 150, OverlapAllDynamic)
- Ajout FountainLight (PointLight) : feedback visuel etat fontaine
- OnBeginOverlap : Cast HC -> Branch(bIsActivated) -> True : couleur chaude (R=1.0,G=0.8,B=0.3, intensite 2000) / False : couleur froide (R=0.3,G=0.5,B=1.0, intensite 500)
- OnEndOverlap : retour couleur froide dans tous les cas
- Feedback activation immediate : BP_FountainComponent pousse SetIntensity+SetLightColor sur FountainLight a l'activation (sans attendre EndOverlap/BeginOverlap)

#### BP_FountainComponent -- refacto majeure -- VALIDE PIE
- Suppression overlap automatique -- interaction volontaire via BPI_Interactable.Interact
- OnPlayerInteract : Branch(bIsActivated)
  - False (1ere activation) : SET bIsActivated=true -> GetOwner -> FountainLight couleur chaude -> Cast GameMode -> OnFountainRest(FountainID)
  - True (suivantes) : GetPlayerController -> Cast PC -> CreateWidget(UI_FountainMenu, OwningPlayer=PC) -> AddToViewport -> GetSubsystem -> RemoveIMC(IMC_Gameplay) -> AddIMC(IMC_Menu) + SetShowMouseCursor=true + SetInputModeUIOnly
- BPI_Saveable implemente : SaveData -> Array_Add(FountainID) dans SaveGame.ActivatedFountains / LoadData -> Array_Contains(FountainID) -> SET bIsActivated

#### BP_SaveGame_SoM -- ajout variable
- Ajout ActivatedFountains (TArray<FName>) -- liste des fontaines activees entre sessions

#### UI_FountainMenu -- VALIDE PIE
- Path UE5 : /Game/UI/Widgets/FountainMenu/UI_FountainMenu
- Structure : Canvas Panel -> Vertical Box -> Text "FONTAINE DE FEE" + Btn_SeReposer + Btn_MenuInventaire
- Btn_SeReposer : GetOwningPlayer -> Cast PC -> GetGameMode -> Cast GameMode -> OnFountainRest(FountainID=None C1) -> Print stub -> RemoveFromParent -> SetInputModeGameOnly + SetShowMouseCursor=false -> RemoveIMC(IMC_Menu) -> AddIMC(IMC_Gameplay)
- Btn_MenuInventaire : Print "WIP" -> RemoveFromParent -> swap IMC identique
- FountainID stub (None) en C1 -- passer le vrai FountainID via variable sur le widget en C2

#### Bugs resolus
- IMC swap seul insuffisant pour bloquer le mouvement : remplacement par SetInputModeUIOnly/SetInputModeGameOnly + SetShowMouseCursor
- Feedback visuel PointLight ne se mettait pas a jour si activation en restant dans la zone d'overlap : ajout notification directe FountainComponent -> FountainLight au moment SET bIsActivated=true

#### Dettes C1 restantes
- UI_FountainMenu.FountainID hardcode None -- passer le vrai ID via variable widget en C2
- Btn_MenuInventaire stub vide -- contenu a ENEMY-Base + jalon dedie
- Se reposer : respawn ennemis zone non implemente (stub log) -- a MAP-C1Level
- Se reposer : PurgeCorruption non branche -- a connecter (oubli C1, corriger avant ENEMY-Base)
- BPI_Interactable : priorite entre interactables superposees non geree -- a UI-InteractPriority C2

#### Etat final
UI-FountainMenu VALIDE PIE. Interaction volontaire fontaine, feedback PointLight bIsActivated, menu deux boutons fonctionnel, persistance bIsActivated via BPI_Saveable.

---

### 06/06/2026 -- ENEMY-DropSystem -- VALIDE PIE

#### Architecture drops -- decisions de design
- Essence ennemi : comportement actif DS-like (vole vers le hero automatiquement) -- distinct de BP_EssenceDrop (passif, mort hero)
- BP_EssenceDrop : inchange -- drop passif au sol, mort hero uniquement, overlap joueur
- BP_EssenceOrb : nouvel Actor -- drop actif, mort ennemi, vol automatique vers hero via VInterpTo
- BP_ItemDrop : stub visuel C1, x% chance, overlap -> DestroyActor uniquement (pas d'inventaire)
- Separation explicite : deux Actors distincts plutot qu'un bool bAutoFly -> architecture propre
- Calibrage C2 : DataTable drops (type ennemi) + multiplicateur Corruption + lien InventoryComponent

#### BP_EssenceOrb -- VALIDE PIE
- Composants : SphereComponent (root), StaticMesh (NoCollision), PointLight
- Variables : EssenceDropValue (int64), TargetCharacter (HC ref), FlySpeed (float), ArrivalThreshold (float)
- BeginPlay : GetPlayerCharacter -> Cast HC -> SET TargetCharacter
- Tick : IsValid(TargetCharacter) -> VInterpTo(SelfPos, TargetPos, DeltaSeconds, FlySpeed) -> SetActorLocation
- VSize(Target - Self) < ArrivalThreshold -> OnArrival
- OnArrival : GetStatValue(EssenceValue) + EssenceDropValue -> Conv_Int64ToDouble -> SetStatValue(EssenceValue) -> DestroyActor
- Path UE5 : /Game/Systems/Essence/BP_EssenceOrb

#### BP_Enemy_Base -- modifications VALIDE PIE
- OnDeath -> SpawnActor(BP_EssenceOrb, GetActorLocation) -> SET EssenceDropValue (hardcode 15 en C1)
- RandomFloatInRange(0,1) > 0.5 -> Branch true : SpawnActor(BP_ItemDrop) -- stub, branche non connectee en C1
- EssenceDropValue hardcode C1 -- migrer vers DT_Enemy en C2
- ItemDropChance hardcode 0.5 C1 -- migrer vers DT_Item en C2

#### UI_HUD_Main -- fix affichage Essence
- Bug : EssenceValue affichait des decimales
- Cause : UpdateStatText utilisait Conv_DoubleToString au lieu de Conv_DoubleToInt64 -> Conv_Int64ToString
- Fix : correction dans UpdateStatText + ajout call UpdateStatText dans HUD_OnStatChanged
- Bug 2 : HUD_OnStatChanged n'appelait pas UpdateStatText -> Essence jamais rafraichi au pickup
- Fix 2 : ajout call UpdateStatText apres RefreshAllStats dans HUD_OnStatChanged

#### Bugs resolus pendant la session
- BP_EssenceOrb condition arrivee inversee (> au lieu de <) -> Orb disparaissait au spawn
- VLerp alpha = DeltaSeconds * FlySpeed > 1 -> Orb depassait la cible et oscillait -- remplace par VInterpTo
- FlySpeed default 0.0 -> Orb immobile -- valeur a regler dans Details panel

#### Etat final
ENEMY-DropSystem VALIDE PIE. Tuer un ennemi spawne un BP_EssenceOrb qui vole vers le hero, credite l'Essence et met a jour le HUD.

---

### 05/06/2026 -- DESIGN-ReplanificationC1 -- session design

#### Etat final
Session design pure. Aucun Blueprint modifie. Roadmap, CLAUDE.md et Decisions.md mis a jour.

---

### 04/06/2026 -- SYS-StatSystem -- VALIDE PIE

#### Etat final
SYS-StatSystem VALIDE PIE complet. Tous les systemes C1 core valides.

---

### 03/06/2026 -- SYS-SaveGame -- VALIDE PIE

#### Etat final
SYS-SaveGame VALIDE PIE. Overlap Fontaine -> save + restauration HP/ST/MP/Corruption. Mort -> drop Essence -> respawn Fontaine. Premiere mort sans save -> respawn PlayerStart.

---

### 02/06/2026 -- SYS-EssenceMana -- VALIDE PIE

#### Etat final
BP_EssenceDrop VALIDE PIE. Mort -> drop Essence + fade -> respawn. Pickup -> restitution Essence + HUD.

---

### 31/05/2026 -- SYS-CorruptionSystem -- VALIDE PIE

#### Etat final
BP_CorruptionComponent VALIDE PIE. TrackDeityUsage, PurgeCorruption, GetWeakDeity operationnels.

---

### 31/05/2026 -- COMBAT-SwordMoveset -- CLOS VALIDE PIE

#### Etat final
Combo epee fonctionnel (Light x2 + Heavy x1). TenaciteEtat dans AttributeSet (base 25).

---

### 31/05/2026 -- SaveDesign + C1-HUDCore -- VALIDE

---

### 30/05/2026 -- DESIGN-WeaponProgression -- VALIDE

---

### 29/05/2026 -- Session design Lore + C1-WeaponArchitecture -- CLOTURE

---

### 28/05/2026 -- Sessions design -- Stats / StatusEffects / Corruption / Economy / Lore

---

### 27/05/2026 -- C1-CleanupDettes + MagicUnlockSystem + RadialUnlock -- VALIDE PIE

---

### 25-26/05/2026 -- Data layer deites + Magic_Progression DESIGN

---

### 23/05/2026 -- C1-InputsUI COMPLET -- VALIDE PIE

---

### 18-21/05/2026 -- CollisionFix / HitFeel / ComboFix / TestBed / LockMove

---

### 17/05/2026 -- J-Camera COMPLET -- VALIDE PIE

---

### 15/05/2026 -- J-lock + J-Renommage COMPLET

---

### 14/05/2026 -- Session design Roadmap + J-Nettoyage + ART + MUS

---

### 12-13/05/2026 -- J-13 Radial Menu + J-15 HUD_Main + J-10 a J-14 POC Magie

---

### 11/05/2026 -- Sessions design + jalons #8 et #9

### 07/05/2026 -- Jalons #1 a #7

### 2025 -- Sessions fondatrices (voir historique complet)

---

## Rappel
Pour la roadmap detaillee : voir Docs/Roadmap_Gameplay.md
Pour les decisions architecturales : voir Docs/Architecture/Decisions.md
Pour les stats et progression : voir Docs/Architecture/Stats_Progression.md
Pour les effets de statut et corruption : voir Docs/Architecture/Combat_StatusEffects.md
Pour l'economie et les drops : voir Docs/Architecture/Economy_Drops.md
Pour le lore et la narrative : voir Docs/Lore_ShadowOfMana.md
Pour la progression armes : voir Docs/Architecture/Weapons_Progression.md
Pour le systeme de save : voir Docs/Architecture/SaveSystem.md

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 09/06/2026
