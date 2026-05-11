# CLAUDE.md -- Shadow of Mana / Contexte IA

Ce fichier est lu par Claude au debut de chaque session pour retrouver le contexte du projet rapidement.

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

## Conventions de travail

### Git
```
git add .
git commit -m "description courte et coherente"
git push
```
-> Nico pushe d'abord, puis Claude committe le journal via GitHub MCP
-> Claude fournit systematiquement les commandes git + phrase de commit a chaque jalon

### Journal
- Fichier : `Docs/Journal_Modifications.md`
- Claude le met a jour apres chaque jalon via GitHub MCP
- SHA recupere dynamiquement avant chaque commit

### Documentation
- Toute nouvelle feature -> doc dans `Docs/Architecture/`
- Docs d'archi mises a jour systematiquement apres chaque jalon
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

## Comment demarrer une session

1. Nico dit : "on travaille sur Shadow of Mana, lis le CLAUDE.md et le journal"
2. Claude lit ce fichier + `Docs/Journal_Modifications.md`
3. Claude fait un resume de l'etat du projet et propose la suite logique

---

*Derniere mise a jour : 11/05/2026*
