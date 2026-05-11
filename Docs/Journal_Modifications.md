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
- Get_HealthBar_Percent / Get_StaminaBar_Percent / Get_ManaBar_Percent : simplifiees, retournent la variable locale
- Event Construct : Bind HUD_OnStatChanged sur AttributeSetRef.OnStatChanged
- HUD_OnStatChanged : Switch on Name -> division Current/Max -> SET *Percent correspondant
- InitHUD : fonction d'init appelee depuis Add_Main_HUD apres Add to Viewport
- Add_Main_HUD (BP_PlatformingCharacter) : appel InitHUD apres creation widget

#### Architecture UI -- etat final
- Zero polling : les barres ne lisent plus les stats chaque frame
- Push pur : OnStatChanged notifie le HUD uniquement quand une stat change
- SetStatValue = unique point de modification, garantit la notification
- Extensible : tout nouvel abonne (minimap, boss bar) se bind sur OnStatChanged sans toucher le core

#### Note architecture -- Sauvegarde future
- Les valeurs Current ne sont pas dans la Datatable (valeurs de reference statiques)
- Pour save/load (reprise boss, checkpoint) : prevoir un SaveGame Object dedie
- Au load : reinjecter les Current via SetStatValue pour notifier tous les abonnes

### 10/05/2026 -- Nico + Claude -- Jalon #7 -- Hit Flash ennemi (partiel) + fix GameMode

#### M_Mannequin
- HitFlashAmount (Scalar Parameter, default 0.0) ajoute via MCP Python
- Branche sur Emissive Color via Add (combine avec Emissive existant Logo/EmissivePower)
- Note : materiau temporaire (mannequin Quinn), a refaire sur le vrai enemy mesh

#### BP_EnemyBase
- ReceiveDamage : Set Scalar Parameter Value on Materials HitFlashAmount 1.0 -> Delay 0.12 -> 0.0
- Note : non fonctionnel sur MI_Quinn (Material Instance) -- necessite DMI au BeginPlay
- A finaliser quand le vrai enemy mesh/materiau sera en place

#### Fix critique -- BP_SoM_GameMode
- Player Controller Class n'etait pas assigne a BP_PlatformingPlayerController
- Lock-On et Menu Radial ne repondaient plus suite au nettoyage jalon #4
- Corrige : BP_SoM_GameMode -> Player Controller Class = BP_PlatformingPlayerController

### 11/05/2026 -- Nico + Claude -- Jalon stable #8 -- Migration UE5.7 + UnrealClaude

#### Migration moteur
- Projet migre de UE5.6 vers UE5.7.4-51494982
- UnrealGenAISupport (ancien plugin MCP Python/unreal-handshake) supprime
- Migration effectuee via ouverture directe dans UE5.7 (Convert in-place)

#### UnrealClaude v1.4.5
- Repo clone : https://github.com/Natfii/UnrealClaude (avec --recurse-submodules)
- Compilation : RunUAT.bat BuildPlugin -MaxParallelActions=2 (limite RAM) -- succes en 67s
- Installation : Plugins/UnrealClaude/ dans le projet
- MCP bridge : npm install dans Resources/mcp-bridge (151 packages)
- Validation : curl http://localhost:3000/mcp/status -> 28 outils operationnels
- Panel Tools -> Claude Assistant operationnel dans l'editeur UE5.7
- Authentification : claude auth login (compte Pro, pas d'API key separee)

#### Setup technique nouveau -- etat final
- Claude Code CLI v2.1.138 installe globalement (npm install -g @anthropic-ai/claude-code)
- UnrealClaude : MCP bridge Node.js port 3000 (auto-start au lancement editeur)
- 28 outils MCP : Blueprint, AnimBlueprint, Enhanced Input, Material, Actor, Level, Asset...
- Plus de dependance Python / fastmcp / socket port 9877
- GitHub MCP : inchange (node.exe --use-system-ca, token Classic scope repo)

### 11/05/2026 -- Nico + Agent UE -- Jalon #9 -- Audit complet + nettoyage Priorite 1 et 2

#### Audit complet du projet (agent UnrealClaude -- lecture seule)
- Analyse filesystem, configs, plugins, structure assets
- 4 critiques, 5 importants, 5 mineurs identifies
- Rapport complet dans Docs/Session_UnrealClaude.md

#### Fixes Priorite 1 (Claude.ai via GitHub MCP -- fichiers texte)
- Config/DefaultGame.ini : suppression section GenerativeAISupportSettings (C1)
- Config/DefaultGame.ini : ProjectName = Shadow of Mana (I3)
- SoM_250617.uproject : declaration officielle UnrealClaude (C2)

#### Nettoyage Priorite 2 (agent UE -- filesystem, references verifiees)
- Supprime : Content/ThirdPerson/ entier (BP_ThirdPersonCharacter, BP_ThirdPersonGameMode, Lvl_ThirdPerson, MI_ThirdPersonColWay) -- 0 reference externe (C3)
- Supprime : IA_TestFloat, IA_Test_AttachWaepon, IA_UI_TestFloat -- 0 reference externe (I5)

### 11/05/2026 -- Nico -- Fix C4 : Lvl_Platforming GameMode Override

#### Lvl_Platforming
- World Settings -> GameMode Override : BP_PlatformingGameMode -> BP_SoM_GameMode
- Risque elimine : Lock-On et Radial Menu sont desormais garantis sur cette map
- BP_PlatformingGameMode peut etre supprime lors de la prochaine session de nettoyage

#### Roadmap mise a jour
- [x] Migration UE5.7 + UnrealClaude
- [x] Audit complet + nettoyage Priorite 1 et 2
- [x] Fix C4 : Lvl_Platforming GameMode Override corrige
- [ ] Nettoyage final editeur : supprimer BP_PlatformingGameMode (Content Browser)
- [ ] Fix I1 : Consolidation animations en double (session editeur)
- [ ] Fix I2 : Verification et consolidation IMC (session editeur)
- [ ] Fix I4 : Reorganisation dossier Enemies (session editeur)
- [ ] Hit Flash ennemis (vrai enemy mesh + M_Enemy_Base + DMI)
- [ ] Systeme de sauvegarde SaveGame
- [ ] Setup ComfyUI generation textures/concepts (RTX 3080Ti)

---

## Rappel
Ce document doit etre mis a jour a chaque modification significative.

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 11/05/2026
