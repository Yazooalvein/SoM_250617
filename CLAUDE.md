# CLAUDE.md -- Shadow of Mana / Contexte IA

Ce fichier est lu par Claude au debut de chaque session pour retrouver le contexte du projet rapidement.
Il est lu aussi bien par Claude.ai (via GitHub MCP) que par l'agent UnrealClaude dans l'editeur UE5.7.

---

## Projet

- **Nom** : Shadow of Mana (SoM)
- **Genre** : ARPG Blueprint Only, inspire Secret of Mana + Dark Souls
- **Developpeur** : Nico (GitHub : Yazooalvein)
- **Repo** : https://github.com/Yazooalvein/SoM_250617
- **Moteur** : Unreal Engine 5.7.4

---

## Setup technique actuel Claude <> Projet

- **UnrealClaude v1.4.5** (plugin dans Plugins/UnrealClaude/)
  - Claude Code CLI v2.1.138 (`npm install -g @anthropic-ai/claude-code`)
  - Authentification via `claude auth login` (compte Anthropic Pro -- pas d'API key separee)
  - MCP bridge Node.js port 3000 (auto-start au lancement editeur)
  - 28 outils MCP natifs : Blueprint, AnimBlueprint, Enhanced Input, Material, Actor, Level, Asset...
  - Panel : Tools -> Claude Assistant dans l'editeur UE5.7
- **GitHub MCP** : node.exe --use-system-ca + NODE_TLS_REJECT_UNAUTHORIZED=0
  - Token Classic scope `repo` complet
- **Claude** : plan Pro, memoire activee

### Notes installation (pour reference)
- Compilation depuis sources obligatoire (pas de binaires precompiles)
- RunUAT.bat BuildPlugin avec -MaxParallelActions=2 (limite RAM sur cette machine)
- npm install dans Resources/mcp-bridge apres copie dans Plugins/
- Validation : `curl http://localhost:3000/mcp/status`

---

## Workflow dual-agent

Ce projet utilise deux instances Claude complementaires qui ne se voient pas en temps reel.
Ce fichier (CLAUDE.md) est le point de synchronisation central entre les deux.

### Roles

**Claude.ai (chef de projet)**
- Lit le repo via GitHub MCP au debut de chaque session
- Planification, decisions d'architecture, roadmap
- Met a jour Journal_Modifications.md et CLAUDE.md apres chaque jalon
- Lit Session_UnrealClaude.md pour rester au courant de ce que l'agent UE a fait

**Agent UnrealClaude (bras droit dans l'editeur)**
- Modifications Blueprint directes (variables, nodes, connections, materials)
- Queries temps reel sur assets, acteurs, niveaux
- Logue systematiquement ses actions dans Docs/Session_UnrealClaude.md
- Lit CLAUDE.md au demarrage pour connaitre l'architecture et les conventions

### Regles de synchronisation

1. **Nico pushe toujours en premier**, Claude.ai committe la doc ensuite (jamais l'inverse)
2. **L'agent UE logue ses actions** dans Docs/Session_UnrealClaude.md en temps reel
3. **Claude.ai lit Session_UnrealClaude.md** en debut de session pour rattraper ce qui a ete fait dans UE
4. **Apres chaque jalon significatif** : Nico push -> Claude.ai met a jour Journal + CLAUDE.md

### Deroulement type d'une session

```
DEBUT DE SESSION :
1. Nico ouvre claude.ai
2. Nico dit "on travaille sur SoM, lis le CLAUDE.md et le journal"
3. Claude.ai lit CLAUDE.md + Journal_Modifications.md + Session_UnrealClaude.md
4. Claude.ai fait un resume complet et propose la suite

PENDANT LA SESSION :
5. Nico ouvre UE5.7 + panel Claude Assistant
6. Agent UE travaille sur les Blueprints, logue dans Session_UnrealClaude.md
7. Claude.ai reste disponible pour decisions d'archi et questions

FIN DE JALON :
8. Nico : git add . && git commit -m "..." && git push
9. Claude.ai : met a jour Journal_Modifications.md + CLAUDE.md via GitHub MCP
```

---

## Instructions pour l'agent UnrealClaude

**A lire et appliquer des le debut de chaque session dans l'editeur.**

### Logging obligatoire

Apres chaque modification significative, tu dois ecrire dans `Docs/Session_UnrealClaude.md`.
Utilise l'outil Write/Edit pour maintenir ce fichier a jour en temps reel.

Format d'entree a respecter :

```
### [DATE] -- [NOM DU BLUEPRINT / ASSET]
**Action** : ce qui a ete fait (ajout variable, nouveau node, connexion, etc.)
**Pourquoi** : raison ou contexte
**Points d'attention** : gotchas, dependances, ce qui pourrait casser
```

### Conventions architecture a respecter (IMPERATIVES)

- `SetStatValue(StatName, Value)` = UNIQUE point de modification des stats. Jamais de SET direct.
- `OnStatChanged` = dispatcher de notification, tous les abonnes (HUD, ennemis) passent par lui
- Nommage stats : sans espace, CamelCase (HealthCurrent, StaminaMax, etc.)
- `BP_SoM_GameMode` : toujours verifier que Player Controller Class = BP_PlatformingPlayerController
- Hit Flash ennemi : utiliser Dynamic Material Instance au BeginPlay, pas Set Scalar on Materials
- Inputs : source unique Content/Input/InputActions/, ne jamais creer de doublons

### Ce que Claude.ai sait et toi non (en temps reel)

Claude.ai a acces a l'historique complet des sessions via GitHub.
Toi tu as acces a l'editeur en temps reel.
Le fichier Session_UnrealClaude.md est le pont entre vous deux.
Maintiens-le scrupuleusement : Claude.ai s'en sert pour etre au courant de tout ce que tu fais.

---

## Conventions de travail

### Git
```
git add .
git commit -m "description courte et coherente"
git push
```
-> Nico pushe d'abord, puis Claude.ai committe le journal via GitHub MCP
-> Claude.ai fournit systematiquement les commandes git + phrase de commit a chaque jalon

### Journal
- Fichier : `Docs/Journal_Modifications.md`
- Claude.ai le met a jour apres chaque jalon via GitHub MCP
- SHA recupere dynamiquement avant chaque commit

### Session UnrealClaude
- Fichier : `Docs/Session_UnrealClaude.md`
- L'agent UE le met a jour en temps reel pendant ses interventions
- Claude.ai le lit en debut de session pour rattraper le contexte

### Documentation architecture
- Toute nouvelle feature -> doc dans `Docs/Architecture/`
- Index : `Docs/Project_Architecture_Index.md`

---

## Architecture cle (resume)

### Personnage
- `BP_PlatformingCharacter` (Blueprint Only)
- Stats via `BP_AttributeSet_Base` (ref : `AttributeSetRef`)
- `bIsDead` (private) + `IsDead()` (public pure)
- `bIsInvincible` (iframes dash/roll, pilote par AnimNotify AN_EndDash/AN_EndRoll)
- `OnPlayerDeath` dispatcher (sans params)
- `OnStatChanged(StatName, NewValue)` dispatcher dans AttributeSet
- `DiscoveredWeapons` (Array<FName>) : liste des armes debloquees (source de verite)

### Stats
- `SetStatValue(StatName, Value)` = unique point de modification (jamais de SET direct)
- Nommage sans espace : HealthCurrent, HealthMax, StaminaCurrent, StaminaMax, ManaCurrent, ManaMax...
- `OnStatChanged` notifie tous les abonnes (HUD, futurs ennemis/boss)

### GameMode / Controllers
- `BP_SoM_GameMode` (`/Game/Core/`) -- Player Controller Class = BP_PlatformingPlayerController
- `BP_PlatformingPlayerController` : gere Lock-On, Menu Radial, IMC_Prototype
- ⚠️ Toujours verifier Player Controller Class dans BP_SoM_GameMode apres toute refonte

### Ennemis
- `BP_EnemyBase` -> `BP_AIController_Enemy_Base`
- Behavior Tree + Blackboard + PawnSensing
- `LoseAggro()` pour desengagement

### Combat
- `BPI_TakeDamage` + `BP_ComboManagerComponent`
- ReceiveDamage : bIsInvincible? -> IsDead? -> SetStatValue("HealthCurrent") -> HitFlash -> mort?

### Armes
- `DT_Weapons` : 2 entrees (Sword_01, 2HSword_01), struct FWeaponData
- `BP_Weapon_Base` : spawn data-driven via GetDataTableRowFromName au BeginPlay
- `EquipWeapon(RowName)` dans BP_PlatformingCharacter : BeginDeferredActorSpawnFromClass + K2_AttachToComponent sur HandGrip_R
- ⚠️ WeaponDataTest : variable debug a supprimer post-J-13

### UI / HUD
- `UI_HUD_Main` : event-driven via OnStatChanged, zero polling -- FINALISE
  - Layout : SizeBox_Weapon (64x64) + HUD_Main_VertBox (HP/ST/MP/XP)
  - UpdateStatText(Current, Max, RichTextBlock) : affiche "X / Y" sans decimales
  - InitHUD : init barres ET textes au demarrage
  - DT_HUD_RichTextStyle : Content/UI/Widgets/Main/
  - ⚠️ SizeBox obligatoire autour de chaque ProgressBar
  - ⚠️ Size To Content sur HUD_Anchor doit etre DECOCHE
- `UI_Enemy_HealthBar`, `UI_LockOnIndicator`

### Radial Menu -- J-13 QUASI-COMPLET
- Chemin assets : Content/UI/Widgets/RadialMenu/
- `ERadialMode` : enum Weapons / Magic
- `FSoM_RadialSlotData` : struct SlotID, DisplayName, Description, Icon, Category, StatA/B/C
- `UI_RadialSlot` : widget slot 80x80, SetSelected(bool) + SetSlotData(FSoM_RadialSlotData)
- `UI_RadialSlot_OLD` : ancien widget slot (conserve, non utilise, renomme)
- `UI_Radial_Main` : widget radial principal -- VALIDE PIE
  - Variables : CurrentCategory, SelectedIndex, SlotWidgets, SlotDataList
  - RadialRadius = 330, RadialContainer Size = 0.01x0.01 (fix drift)
  - TargetRotation, CurrentRotation, InterpSpeed(8.0)
  - GenerateSlots() : Cos/Sin positioning, slots en cercle autour RadialContainer
  - UpdateCenterInfo() : SET Text_ItemName/Description/Category depuis SlotDataList[SelectedIndex]
  - UpdateSelection(AxisValue) : navigation par cran
    - Branch AxisValue > 0 : SelectedIndex+1, TargetRotation+AnglePerSlot
    - Branch AxisValue < 0 : SelectedIndex-1, TargetRotation-AnglePerSlot
    - Wrap : (SelectedIndex + NbSlots) % NbSlots
    - ForEach SlotWidgets -> SetSelected(ArrayIndex == SelectedIndex) -> UpdateCenterInfo
  - Event Tick : FInterpTo(CurrentRotation->TargetRotation) -> SetRenderTransformAngle(RadialContainer)
    + contre-rotation icones (CurrentRotation * -1)
  - Event Construct : PopulateWeaponSlots -> GenerateSlots -> UpdateCenterInfo -> SetSelected(slot 0)
  - PopulateWeaponSlots() : DiscoveredWeapons -> GetDataTableRow(DT_Weapons) -> FSoM_RadialSlotData
  - SwitchCategory(Direction) : toggle Weapons/Magic -> PopulateWeaponSlots ou TODO Magic
    + reset SelectedIndex/TargetRotation/CurrentRotation = 0
  - ValidateSelectedWeapon() : SlotDataList[SelectedIndex].SlotID -> EquipWeapon -> CloseRadialMenu
  - RESTE A FAIRE : UI_QuickslotBar
  - ⚠️ Dette : surbrillance devrait se placer sur l'arme equipee a l'ouverture (pas slot 0)
  - ⚠️ Dette : comportement categorie Magic a definir
- `BP_PlatformingPlayerController` :
  - `OpenRadialMenu` : IsValid guard + Create UI_Radial_Main + Time Dilation 0.2 + Add to Viewport
    + Set Input Mode Game And UI (WidgetToFocus = RadialMainRef)
  - `CloseRadialMenu` : Remove from Parent + Time Dilation 1.0 + Input Mode Game Only
  - `Handle_UI_RadialMenu_Rotate` : IsValid(RadialMainRef) -> UpdateSelection(AxisValue)
  - `Handle_UI_RadialMenu_ChangeCat` : IsValid(RadialMainRef) -> SwitchCategory(RadialMainRef)
  - `IA_validate_radial_selection` : IsValid(RadialMainRef) -> ValidateSelectedWeapon
  - `IA_UI_Radial_Cancel` : IsValid(RadialMainRef) -> CloseRadialMenu
  - `RadialMainRef` (UI_Radial_Main) : variable de reference principale
  - ⚠️ Ancienne logique UI_RadialMenu presente mais deconnectee -- a nettoyer post-J-13

### Inputs (IMC_Prototype)
- Source unique : `Content/Input/InputActions/`
- IMC actifs : IMC_Default, IMC_Platforming, IMC_Prototype
- IA_UI_RadialMenu_Rotate : Axis1D (Q/D + Gamepad Right Thumbstick X)
- IA_UI_RadialMenu_ChangeCat : Axis1D (Gamepad Left Thumbstick Y)
- IA_validate_radial_selection : Axis1D (Bouton A/X gamepad)
- IA_UI_Radial_Cancel : (Bouton B/Circle + Escape)
- ⚠️ Dette : creer IMC_UI dedie pour les inputs menus, clean IMC_Prototype (prevu post-J-13)

### Magie
- `BP_MagicComponent` : UnlockedSpells, QuickslotSlots, SpellCooldowns, CastSpell
- `BP_SpellBase` + 4 sorts Lumina valides PIE (Heal, Attack, Buff, Debuff)
- `DT_Spells` + structs FSoM_SpellData / FSoM_DeitySpells
- Chemin assets : Content/Systems/Magic/

---

## Jalons completes

- [x] #1 a #9 : MCP, mort, stats, inputs, iframes, UI, hit flash, migration UE5.7, audit
- [x] J-10/11/12 : BP_MagicComponent complet
- [x] J-14 : BP_SpellBase + 4 sorts Lumina valides PIE
- [x] J-15 : UI_HUD_Main finalise
- [x] J-13 WIP : radial navigation + PopulateWeaponSlots + SwitchCategory + ValidateSelectedWeapon + Cancel

## Roadmap immediate

- [ ] J-13 final : UI_QuickslotBar (3 slots HUD)
- [ ] Refactorer BP_Spell_Buff/Debuff AffectedStat dynamique (dette)
- [ ] UnlockDeity data-driven depuis DT_Spells (dette)
- [ ] Hit Flash ennemis (vrai mesh + M_Enemy_Base + DMI)
- [ ] IMC_UI dedie + clean IMC_Prototype (dette)
- [ ] SaveGame
- [ ] ComfyUI textures (RTX 3080Ti)

---

## Notes techniques importantes

- Hit Flash ennemi : DMI au BeginPlay + Set Scalar sur DMI
- `BP_SoM_GameMode` : Player Controller Class = BP_PlatformingPlayerController obligatoire
- RichTextBlock : necessite DataTable (RichTextStyleRow) assignee dans Text Style Set
- ProgressBar dans HBox/VBox : toujours wrapper dans SizeBox pour controler la hauteur
- To Text (Float) : Max/Min Fractional Digits = 0 pour supprimer les decimales
- Radial : ancienne logique UI_RadialMenu deconnectee mais conservee -- a nettoyer
- Time Dilation 0.2 a l'ouverture radial, 1.0 a la fermeture (remplace Set Game Paused)
- Widget "Is Variable" obligatoire pour acceder depuis le graph
- Make Brush from Texture + Set Brush pour assigner une Texture2D a une Image widget
- Radial navigation : TargetRotation s'accumule (pas de % 360) pour lerp correct
- Radial wrap index : (SelectedIndex + NbSlots) % NbSlots
- Radial drift fix : RadialContainer Size = 0.01x0.01 (pivot quasi-ponctuel)
- IsValid(RadialMainRef) guard obligatoire avant tout appel sur le radial depuis le PC

---

## Comment demarrer une session claude.ai

1. Nico dit : "on travaille sur Shadow of Mana, lis le CLAUDE.md et le journal"
2. Claude.ai lit ce fichier + `Docs/Journal_Modifications.md` + `Docs/Session_UnrealClaude.md`
3. Claude.ai fait un resume complet (jalons, dernieres actions UE) et propose la suite logique

## Comment demarrer une session UnrealClaude (dans l'editeur)

1. Ouvrir Tools -> Claude Assistant
2. Dire : "lis le CLAUDE.md du projet et logue tes actions dans Docs/Session_UnrealClaude.md"
3. L'agent lit le contexte, confirme les conventions, et commence a travailler

---

*Derniere mise a jour : 13/05/2026*
