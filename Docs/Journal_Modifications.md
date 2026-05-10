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

#### Roadmap mise a jour
- [x] Mort joueur : OnPlayerDeath + desengagement ennemis
- [x] OnStatChanged Event Dispatcher dans BP_AttributeSet_Base
- [x] Unification des inputs dupliques
- [x] Iframes dash/roll (bIsInvincible, pilote par AnimNotify)
- [x] OnStatChanged -> bindings UI event-driven (zero polling)
- [ ] Hit Flash ennemis
- [ ] Systeme de sauvegarde SaveGame (session dediee)
- [ ] Migration UE5.7 + UnrealClaude (session dediee)
- [ ] Setup ComfyUI pour generation textures/concepts

---

### [A completer apres chaque evolution]

---

## Rappel
Ce document doit etre mis a jour a chaque modification significative.

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 10/05/2026
