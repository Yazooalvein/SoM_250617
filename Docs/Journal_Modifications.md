# Journal des Modifications -- Shadow of Mana

## Objectif
Suivi precis de toutes les evolutions majeures du projet.

## Entrees

### 17/06/2025 -- Nico -- Creation du projet
- Initialisation SoM sous UE5.6, template Third Person Platforming
- Creation docs de base

### 18/06/2025 -- Nico
- Refactoring pipeline Gameplay de base (Dash, Roll, Jump, Stamina)

### 19-20/06/2025 -- Nico
- Lock-On, Menu Radial, refonte Combo

### 21/06/2025 -- Nico
- Refactorisation BP_ComboManagerComponent (TMap, fenetre dynamique)

### 24/06/2025 -- Nico
- Systeme armes data-driven, Menu Radial data-driven, Combo multi-armes

### 26/06/2025 -- Nico -- Systeme degats
- BPI_TakeDamage, BP_EnemyBase ReceiveDamage + OnDeath

### 27/06/2025 -- Nico -- IA ennemis
- BP_AIController_Enemy_Base, PawnSensing, aggro/perte

### 20/07/2025 -- Nico -- Animation Weapon Integration

### 07/05/2026 -- Nico + Claude -- Jalon stable #1 -- Setup MCP + Hit Flash joueur
- Pipeline Claude Desktop + MCP unreal-handshake operationnel
- GitHub MCP operationnel (SSL fix, node.exe --use-system-ca)
- M_Hero : HitFlashAmount sur Emissive via Python MCP
- BP_PlatformingCharacter > ReceiveDamage : flash blanc 0.12s
- Revue technique complete, priorites identifiees

### 07/05/2026 -- Nico + Claude -- Jalon stable #2 -- Mort du joueur
- BP_SoM_GameMode cree (remplace BP_PlatformingGameMode)
- bIsDead, IsDead(), OnPlayerDeath dispatcher, AM_Death
- ReceiveDamage : check bIsDead + pipeline mort complet
- BP_EnemyBase : bind OnPlayerDeath -> LoseAggro
- Architecture propre : un point de blocage + dispatcher

### 07/05/2026 -- Nico + Claude -- Jalon stable #3 -- OnStatChanged

#### BP_AttributeSet_Base
- Event Dispatcher OnStatChanged(StatName [Name], NewValue [Float])
- SetStatValue : Call OnStatChanged apres le Switch, branché sur tous les SET
- StatName et Value passes directement depuis les inputs de SetStatValue
- Un seul node Call pour tous les cases du Switch
- Dispatcher pret a etre utilise par UI, ennemis, boss, effets de seuil

#### Architecture Stat System -- etat final priorites hautes
- SetStatValue = unique point de modification des stats
- OnStatChanged = notification event-driven vers tous les abonnes
- UI peut se binder pour remplacer le polling continu
- Extensible pour ennemis/boss/compagnons sans modification du core

### 08/05/2026 -- Nico + Claude -- Jalon stable #4 -- Unification inputs

#### Nettoyage vestiges template ThirdPerson
- Supprime : BP_ThirdPersonGameMode + BP_ThirdPersonCharacter (vestiges template inutilises)
- Supprime : Content/Input/Actions/ (doublons IA_Jump, IA_Look, IA_Move, IA_Dash, IA_MouseLook)
- Supprime : IMC_MouseLook (lie uniquement aux vestiges supprimes)

#### Architecture Input -- etat final
- Source unique : Content/Input/InputActions/ (IA_Jump, IA_Look, IA_Move, IA_Dodge, IA_Sprint, IA_LockOn, IA_Attack_Light, IA_Attack_Heavy, IA_Block, IA_RadialMenu...)
- IMC actifs : IMC_Default, IMC_Platforming, IMC_Prototype
- BP_PlatformingCharacter + BP_PlatformingPlayerController = seuls consommateurs des inputs

#### Roadmap mise a jour
- [x] Mort joueur : OnPlayerDeath + desengagement ennemis
- [x] OnStatChanged Event Dispatcher dans BP_AttributeSet_Base
- [x] Unification des inputs dupliques : source unique Content/Input/InputActions/
- [ ] Iframes dash/roll (bIsInvincible dans ReceiveDamage)
- [ ] OnStatChanged -> bindings UI event-driven
- [ ] Hit Flash ennemis
- [ ] Migration UE5.7 + UnrealClaude (session dediee)
- [ ] Setup ComfyUI pour generation textures/concepts

---

### [A completer apres chaque evolution]

---

## Rappel
Ce document doit etre mis a jour a chaque modification significative.

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 08/05/2026
