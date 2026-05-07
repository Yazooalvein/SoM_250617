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

#### BP_SoM_GameMode cree
- Herite de GameModeBase, Default Pawn = BP_PlatformingCharacter
- Remplace BP_PlatformingGameMode dans Project Settings
- BeginPlay : bind OnPlayerDeath -> HandlePlayerDeath
- HandlePlayerDeath : Delay 2s -> Open Level (current)

#### Mort du joueur -- BP_PlatformingCharacter
- Variable bIsDead (Bool, private, default false)
- Fonction pure IsDead() exposee publiquement
- Event Dispatcher OnPlayerDeath (sans parametres)
- ReceiveDamage : check bIsDead en tete (return si true)
- ReceiveDamage apres degats : Branch CurrentHealth <= 0
  -> bIsDead = true, Disable Input, Play AM_Death, Delay 2s, Call OnPlayerDeath
- AM_Death : AnimMontage cree depuis MM_Death_Back_01

#### Desengagement ennemis a la mort du joueur
- BP_EnemyBase > BeginPlay : bind OnPlayerDeath -> OnPlayerDied
- OnPlayerDied : Get Controller -> Cast BP_AIController_Enemy_Base -> LoseAggro
- LoseAggro reset le Blackboard (TargetActor = None, HasAggro = false) + stoppe le BT
- RegisterTarget : check IsDead deja en place (ne cible pas un joueur mort)
- Architecture : un seul point de blocage (ReceiveDamage) + dispatcher pour comportements

#### Roadmap mise a jour
- [x] Mort joueur : OnPlayerDeath + desengagement ennemis
- [ ] OnStatChanged Event Dispatcher dans BP_AttributeSet_Base
- [ ] Unification des inputs dupliques
- [ ] Iframes dash/roll
- [ ] Migration UE5.7 + UnrealClaude (jalon dedie)
- [ ] Setup ComfyUI pour generation textures/concepts

---

### [A completer apres chaque evolution]

---

## Rappel
Ce document doit etre mis a jour a chaque modification significative.

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 07/05/2026
