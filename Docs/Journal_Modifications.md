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
  - True : damage ignore, exec termine
  - False : flow existant (IsDead? + soustraction HP + HitFlash + mort)
- Dash : SET bIsInvincible = true apres SET IsDashing = true
- Custom Event EndDash (AN_EndDash) : SET bIsInvincible = false apres SET IsDashing = false
- Roll : SET bIsInvincible = true apres SET IsRolling = true
- Custom Event EndRoll (AN_EndRoll) : SET bIsInvincible = false apres SET IsRolling = false

#### Architecture Iframes -- etat final
- Duree iframe = duree animation (AN_EndDash / AN_EndRoll comme points de sortie)
- Un seul flag bIsInvincible partage Dash + Roll
- Approche Dark Souls : c'est l'AnimNotify qui definit la fenetre d'invincibilite
- Extensible : tout futur mouvement peut SET bIsInvincible sans toucher ReceiveDamage

### 10/05/2026 -- Nico + Claude -- Jalon stable #6 -- OnStatChanged bindings UI event-driven

#### BP_AttributeSet_Base
- SetStatValue : ajout cases HealthCurrent, StaminaCurrent, ManaCurrent dans Switch on Name
- Nommage unifie sans espaces : HealthCurrent, StaminaCurrent, ManaCurrent, HealthMax etc.
- ConsumeStamina : SET direct remplace par SetStatValue("StaminaCurrent")
- HandleStaminaRegen : SET direct remplace par SetStatValue("StaminaCurrent")
- ReceiveDamage : SET direct remplace par SetStatValue("HealthCurrent")
- InitAttributesFromDatatable : SET directs Current remplaces par SetStatValue apres Completed

#### UI_HUD_Main
- 3 variables ajoutees : HealthPercent, StaminaPercent, ManaPercent (Float, default 1.0)
- Get_HealthBar_Percent / Get_StaminaBar_Percent / Get_ManaBar_Percent : simplifiees
- Event Construct : Bind HUD_OnStatChanged sur AttributeSetRef.OnStatChanged
- HUD_OnStatChanged : Switch on Name -> division Current/Max -> SET *Percent correspondant
- InitHUD : appelee depuis Add_Main_HUD apres Add to Viewport

#### Architecture UI -- etat final
- Zero polling, push pur via OnStatChanged
- SetStatValue = unique point de modification, garantit la notification

### 10/05/2026 -- Nico + Claude -- Jalon #7 -- Hit Flash ennemi (partiel) + fix GameMode

#### M_Mannequin
- HitFlashAmount (Scalar Parameter, default 0.0) ajoute
- Note : materiau temporaire, a refaire sur vrai enemy mesh

#### BP_EnemyBase
- ReceiveDamage : Set Scalar Parameter HitFlashAmount 1.0 -> Delay 0.12 -> 0.0
- Non fonctionnel sur MI_Quinn -- necessite DMI au BeginPlay

#### Fix critique -- BP_SoM_GameMode
- Player Controller Class = BP_PlatformingPlayerController

### 11/05/2026 -- Nico + Claude -- Jalon stable #8 -- Migration UE5.7 + UnrealClaude

#### Migration moteur
- Projet migre de UE5.6 vers UE5.7.4-51494982
- UnrealGenAISupport supprime, migration via ouverture directe UE5.7

#### UnrealClaude v1.4.5
- Compilation RunUAT.bat -MaxParallelActions=2, succes 67s
- MCP bridge npm install, 28 outils operationnels
- Panel Tools -> Claude Assistant operationnel

### 11/05/2026 -- Nico + Agent UE -- Jalon #9 -- Audit complet + nettoyage

#### Fixes Priorite 1 (Claude.ai)
- DefaultGame.ini : suppression GenerativeAISupportSettings, ProjectName = Shadow of Mana
- SoM_250617.uproject : declaration UnrealClaude

#### Nettoyage Priorite 2 (agent UE)
- Supprime Content/ThirdPerson/ entier (C3)
- Supprime IA_TestFloat, IA_Test_AttachWaepon, IA_UI_TestFloat (I5)

#### Fix C4
- Lvl_Platforming -> World Settings -> GameMode Override = BP_SoM_GameMode

### 11/05/2026 -- Nico + Claude -- Session design + roadmap gameplay
- Lore formalise : Docs/Lore_ShadowOfMana.md
- Roadmap : Docs/Roadmap_Gameplay.md (6 priorites, 32 jalons)
- Architecture magie : Docs/Architecture/Magic_System.md

### 11/05/2026 -- Nico -- Jalon #10/#11 -- Assets systeme magie (POC Magie)

#### Assets crees dans Content/Systems/Magic/
- E_SpellCategory (Enum : Attack, Buff, Debuff, Heal, Ultime)
- E_SpellTarget (Enum : Enemy, Self, Area)
- FSoM_SpellData (Struct : SpellID, SpellName, Deity, Category, ManaCost, CastTime, Cooldown, TargetType, EffectValues, Duration)
- FSoM_DeitySpells (Struct : SpellIDs Array<Name>) -- contournement limite Map<Name, Array<Name>>
- DT_Spells (DataTable, 4 lignes Lumina : Lumina_Heal, Lumina_Attack, Lumina_Buff, Lumina_Debuff)
- BP_MagicComponent (ActorComponent) :
  - Variables : UnlockedSpells (Map<Name, FSoM_DeitySpells>), QuickslotSlots (Array<Name>), SpellCooldowns (Map<Name, Float>), bIsCasting (Boolean)
  - Dispatcher : OnSpellCast(SpellID : Name)
  - Event BeginPlay + Event Tick (Can Ever Tick = true)
  - Ajoute sur BP_PlatformingCharacter comme composant "MagicComponent"

#### Incident technique
- Agent UE a tente d'utiliser execute_script -> crash UE
- Regle : ne jamais utiliser execute_script dans UnrealClaude (blueprint_modify uniquement)
- Tache zombie post-crash resolue par reboot machine (process node orphelin)

#### Roadmap mise a jour
- [x] J-10 : BP_MagicComponent + variables + dispatcher
- [x] J-11 : DT_Spells + Enums + Struct
- [ ] J-12 : Fonctions BP_MagicComponent (CanCast, ConsumeMana, UnlockDeity, IsSpellUnlocked) + BP_SpellBase + enfants Lumina
- [ ] J-13 : UI_RadialMagic (2 niveaux, slow-mo) + UI_QuickslotBar
- [ ] J-14 : Integration complete POC Lumina

---

## Rappel
Ce document doit etre mis a jour a chaque modification significative.
Pour la roadmap detaillee : voir Docs/Roadmap_Gameplay.md

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 11/05/2026
