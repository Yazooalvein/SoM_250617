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
- SetStatValue : Call OnStatChanged apres le Switch, branche sur tous les SET
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
- Source unique : Content/Input/InputActions/
- IMC actifs : IMC_Default, IMC_Platforming, IMC_Prototype
- BP_PlatformingCharacter + BP_PlatformingPlayerController = seuls consommateurs des inputs

### 08/05/2026 -- Nico + Claude -- Jalon stable #5 -- Iframes dash/roll

#### BP_PlatformingCharacter
- Variable bIsInvincible (Boolean, default false) ajoutee
- ReceiveDamage : Branch (bIsInvincible?) insere en premier check
- Dash/Roll : SET bIsInvincible true/false via AnimNotify AN_EndDash/AN_EndRoll

#### Architecture Iframes -- etat final
- Duree iframe = duree animation, approche Dark Souls
- Un seul flag bIsInvincible partage Dash + Roll

### 10/05/2026 -- Nico + Claude -- Jalon stable #6 -- OnStatChanged bindings UI event-driven

#### Architecture UI -- etat final
- Zero polling, push pur via OnStatChanged
- SetStatValue = unique point de modification, garantit la notification

### 10/05/2026 -- Nico + Claude -- Jalon #7 -- Hit Flash ennemi (partiel) + fix GameMode
- M_Mannequin : HitFlashAmount ajoute (temporaire)
- Fix BP_SoM_GameMode : Player Controller Class = BP_PlatformingPlayerController

### 11/05/2026 -- Nico + Claude -- Jalon stable #8 -- Migration UE5.7 + UnrealClaude
- Projet migre UE5.6 -> UE5.7.4
- UnrealClaude v1.4.5 : 28 outils MCP, panel operationnel

### 11/05/2026 -- Nico + Agent UE -- Jalon #9 -- Audit complet + nettoyage
- Fixes Priorite 1 : DefaultGame.ini, ProjectName, uproject
- Nettoyage : ThirdPerson/, IA debug
- Fix C4 : Lvl_Platforming GameMode Override

### 11/05/2026 -- Nico + Claude -- Session design + roadmap gameplay
- Lore formalise : Docs/Lore_ShadowOfMana.md
- Roadmap : Docs/Roadmap_Gameplay.md (6 priorites, 32 jalons)
- Architecture magie : Docs/Architecture/Magic_System.md

### 11/05/2026 -- Nico + Claude -- Jalons #10/#11/#12 -- POC Systeme Magie

#### Assets crees (J-10/J-11) dans Content/Systems/Magic/
- E_SpellCategory, E_SpellTarget (Enums)
- FSoM_SpellData (Struct complete)
- FSoM_DeitySpells (Struct helper -- contournement limite Map<Name, Array<Name>>)
- DT_Spells (DataTable, 4 sorts Lumina)
- BP_MagicComponent (ActorComponent, variables + dispatcher + Tick)
- Ajoute sur BP_PlatformingCharacter comme composant "MagicComponent"

#### Fonctions BP_MagicComponent (J-12)
- UnlockDeity(DeityName) : ajoute les sorts d'une deite dans UnlockedSpells
  - Map Contains -> Branch -> Make FSoM_DeitySpells -> Map Add
  - Lumina hardcode pour le POC : [Lumina_Heal, Lumina_Attack, Lumina_Buff, Lumina_Debuff]
- IsSpellUnlocked(SpellID) -> Boolean (Pure)
  - Map Values -> ForEach -> Break FSoM_DeitySpells -> Array Contains -> bFound
- ConsumeMana(Amount)
  - GetOwner -> Cast BP_PlatformingCharacter -> Get AttributeSetRef -> ManaCurrent - Amount -> SetStatValue("ManaCurrent")
  - Convention respectee : SetStatValue OBLIGATOIRE, jamais SET direct
- CanCast(SpellID) -> Boolean (Pure)
  - NOT bIsCasting AND SpellCooldowns[SpellID] <= 0 AND ManaCurrent >= ManaCost (DT_Spells lookup)
  - Note technique : fonctions Pure incompatibles avec exec pins -> deux AND en chaine

#### BP_PlatformingCharacter BeginPlay
- Ajout en fin de chaine : Get MagicComponent -> UnlockDeity("Lumina")
- Chaine complete : InitAttributes -> AddMainHUD -> InitComboTree -> UnlockDeity

#### Dette technique notee
- UnlockDeity hardcode les SpellIDs de Lumina -- a rendre data-driven via DT_Spells quand plusieurs deites
- CanCast verifie ManaCurrent via DT_Spells lookup -- acceptable pour le POC

#### Incident technique
- Agent UE : execute_script -> crash UE -> INTERDIT definitivement
- Tache zombie resolue par reboot machine (process node orphelin)
- Regle : agent UE = yeux uniquement (blueprint_query, asset_search) -- zero modification

#### Roadmap mise a jour
- [x] J-10 : BP_MagicComponent structure de base
- [x] J-11 : DT_Spells + Enums + Structs
- [x] J-12 : Fonctions BP_MagicComponent + UnlockDeity au BeginPlay
- [ ] J-13 : UI_RadialMagic (2 niveaux, slow-mo 0.15x) + UI_QuickslotBar
- [ ] J-14 : BP_SpellBase + enfants Lumina + integration complete POC

---

## Rappel
Ce document doit etre mis a jour a chaque modification significative.
Pour la roadmap detaillee : voir Docs/Roadmap_Gameplay.md

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 11/05/2026
