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
- `DT_Weapons` + `BP_Weapon_Base`

### UI / HUD
- `UI_HUD_Main` : event-driven via OnStatChanged, zero polling
  - Variables : HealthPercent, StaminaPercent, ManaPercent
  - HUD_OnStatChanged : Switch on Name -> division Current/Max -> SET *Percent
  - InitHUD : appelee depuis Add_Main_HUD apres Add to Viewport
- `UI_Enemy_HealthBar`, `UI_LockOnIndicator`

### Inputs
- Source unique : `Content/Input/InputActions/`
- IMC actifs : IMC_Default, IMC_Platforming, IMC_Prototype
- Vestiges template ThirdPerson supprimes (jalon #4)

---

## Jalons completes

- [x] #1 Setup MCP Claude Desktop <> Unreal + Hit Flash joueur (M_Hero HitFlashAmount)
- [x] #2 Mort du joueur (bIsDead, OnPlayerDeath, AM_Death, LoseAggro)
- [x] #3 OnStatChanged dispatcher dans BP_AttributeSet_Base
- [x] #4 Unification inputs (source unique InputActions/, suppression vestiges ThirdPerson)
- [x] #5 Iframes dash/roll (bIsInvincible, pilote par AnimNotify)
- [x] #6 OnStatChanged -> bindings UI event-driven (zero polling)
- [x] #7 Hit Flash ennemi partiel (M_Mannequin) + fix GameMode PlayerController
- [x] #8 Migration UE5.7 + UnrealClaude v1.4.5 (28 outils MCP, panel editeur)

## Roadmap

- [ ] Hit Flash ennemis (a finaliser avec vrai enemy mesh + M_Enemy_Base + DMI)
- [ ] Systeme de sauvegarde SaveGame
- [ ] Setup ComfyUI generation textures/concepts (RTX 3080Ti)

---

## Notes techniques importantes

- Hit Flash ennemi : utiliser Dynamic Material Instance (BeginPlay) + Set Scalar sur DMI, pas Set Scalar on Materials
- M_Enemy_Base a creer avec HitFlashAmount integre des le depart pour les vrais ennemis
- `BP_SoM_GameMode` : Player Controller Class doit etre BP_PlatformingPlayerController (sinon Lock-On et Radial cassent)
- Substrate material system : verifier statut dans UE5.7 (etait desactive en 5.6)
- Toutes les anims de mort sur SK_Mannequin, retargeter `RTG_NewRetargeter` disponible
- Convention nommage stats : sans espace, CamelCase (HealthCurrent pas "Health Current")
- UnrealClaude : si MCP tools absents -> verifier `npm install` dans mcp-bridge + redemarrer editeur

---

## Comment demarrer une session claude.ai

1. Nico dit : "on travaille sur Shadow of Mana, lis le CLAUDE.md et le journal"
2. Claude.ai lit ce fichier + `Docs/Journal_Modifications.md` + `Docs/Session_UnrealClaude.md`
3. Claude.ai fait un resume complet (jalons, dernières actions UE) et propose la suite logique

## Comment demarrer une session UnrealClaude (dans l'editeur)

1. Ouvrir Tools -> Claude Assistant
2. Dire : "lis le CLAUDE.md du projet et logue tes actions dans Docs/Session_UnrealClaude.md"
3. L'agent lit le contexte, confirme les conventions, et commence a travailler

---

*Derniere mise a jour : 11/05/2026*
